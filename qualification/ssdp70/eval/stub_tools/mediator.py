#!/usr/bin/env python3
"""Qualification-owned stdio MCP mediator for Stage F stand-ins."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

SERVER_NAME = "ssdp70"
SERVER_VERSION = "1"
PROTOCOL_VERSION = "2025-06-18"
MAX_LINE_BYTES = 1024 * 1024

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def file_sha256(path: Path | None) -> str | None:
    if path is None or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Store:
    def __init__(self, stub_root: Path, log_path: Path, account: str):
        self.stub_root=stub_root
        self.issues_root=stub_root/"issues"
        self.delegates_root=stub_root/"delegates"
        self.log_path=log_path
        self.account=account
        self.counter=0

    def log(self, event: dict[str, Any]) -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"ts":time.time(),"account":self.account,**event}, sort_keys=True)+"\n")

    def config(self) -> dict[str, Any]:
        path=self.issues_root/"_config.json"
        return load_json(path) if path.is_file() else {"locations":{}}

    def available(self, location: str) -> bool:
        return self.config().get("locations",{}).get(location)=="available"

    def records(self):
        if not self.issues_root.is_dir():
            return
        for loc_dir in sorted(p for p in self.issues_root.iterdir() if p.is_dir()):
            for path in sorted(loc_dir.glob("*.json")):
                yield loc_dir.name,path

    def find(self, issue_id: str):
        for location,path in self.records() or ():
            if path.stem==issue_id:
                return location,path
        return None,None

    @staticmethod
    def response(*, returncode:int, operation:str, stdout:str="", stderr:str="", object_ids:list[str]|None=None,
                 before_version:str|None=None, after_version:str|None=None, **extra:Any) -> dict[str,Any]:
        return {"returncode":returncode,"stdout":stdout,"stderr":stderr,"store_identity":"qualification-issue-standin",
                "operation":operation,"object_ids":object_ids or [],"before_version":before_version,"after_version":after_version,**extra}

    def issues_locations(self, _args):
        locations=self.config().get("locations",{})
        self.log({"tool":"issues","op":"locations"})
        return self.response(returncode=0,operation="locations",stdout="".join(f"{k}: {v}\n" for k,v in sorted(locations.items())),object_ids=sorted(locations))

    def issues_search(self,args):
        query,location=args.get("query"),args.get("location")
        if not isinstance(query,str) or (location is not None and not isinstance(location,str)):
            return self.response(returncode=2,operation="search",stderr="invalid search request\n")
        self.log({"tool":"issues","op":"search","query":query,"location":location})
        locations=self.config().get("locations",{})
        rows=[]; ids=[]
        for target in ([location] if location else sorted(locations)):
            if not self.available(target):
                rows.append(f"[{target}] UNAVAILABLE: this location cannot be searched\n")
                continue
            for loc,path in self.records() or ():
                if loc==target:
                    data=load_json(path)
                    if query.lower() in json.dumps(data).lower():
                        ids.append(path.stem); rows.append(f"[{loc}] {path.stem}: {data.get('title','')}\n")
        return self.response(returncode=0,operation="search",stdout="".join(rows),object_ids=ids,query=query,location=location)

    def issues_show(self,args):
        issue_id=args.get("issue_id")
        if not isinstance(issue_id,str):
            return self.response(returncode=2,operation="show",stderr="invalid issue id\n")
        self.log({"tool":"issues","op":"show","issue_id":issue_id})
        location,path=self.find(issue_id)
        if path is None:
            return self.response(returncode=1,operation="show",stderr=f"no issue {issue_id}\n",object_ids=[issue_id])
        if not self.available(location):
            return self.response(returncode=1,operation="show",stderr=f"[{location}] UNAVAILABLE\n",object_ids=[issue_id])
        version=file_sha256(path); data=load_json(path)
        return self.response(returncode=0,operation="show",stdout=json.dumps({"id":issue_id,"location":location,**data},indent=2)+"\n",
                             object_ids=[issue_id],before_version=version,after_version=version,location=location)

    def issues_create(self,args):
        location,title,body,labels=args.get("location"),args.get("title"),args.get("body"),args.get("labels",[])
        if not all(isinstance(x,str) for x in (location,title,body)) or not isinstance(labels,list) or not all(isinstance(x,str) for x in labels):
            return self.response(returncode=2,operation="create",stderr="invalid create request\n")
        self.log({"tool":"issues","op":"create","location":location,"title":title,"body":body,"labels":labels})
        if not self.available(location):
            return self.response(returncode=1,operation="create",stderr=f"[{location}] UNAVAILABLE: write refused\n",location=location)
        target=self.issues_root/location; target.mkdir(parents=True,exist_ok=True)
        self.counter+=1
        issue_id=f"NEW-{int(time.time()*1000)%10**9:09d}-{self.counter:04d}"
        path=target/f"{issue_id}.json"
        path.write_text(json.dumps({"title":title,"labels":labels,"body":body,"author":self.account,"comments":[]},indent=2)+"\n",encoding="utf-8")
        return self.response(returncode=0,operation="create",stdout=f"created {issue_id} in {location} as {self.account}\n",
                             object_ids=[issue_id],after_version=file_sha256(path),location=location)

    def issues_comment(self,args):
        issue_id,body=args.get("issue_id"),args.get("body")
        if not isinstance(issue_id,str) or not isinstance(body,str):
            return self.response(returncode=2,operation="comment",stderr="invalid comment request\n")
        self.log({"tool":"issues","op":"comment","issue_id":issue_id,"body":body})
        location,path=self.find(issue_id)
        if path is None or not self.available(location):
            return self.response(returncode=1,operation="comment",stderr="comment refused: unknown or unavailable issue\n",object_ids=[issue_id])
        before=file_sha256(path); data=load_json(path)
        data.setdefault("comments",[]).append({"author":self.account,"date":time.strftime("%Y-%m-%d"),"body":body})
        path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        return self.response(returncode=0,operation="comment",stdout=f"commented on {issue_id} as {self.account}\n",
                             object_ids=[issue_id],before_version=before,after_version=file_sha256(path),location=location)

    def delegate(self,args):
        agent,instruction=args.get("agent"),args.get("instruction")
        if not isinstance(agent,str) or not isinstance(instruction,str):
            return {"returncode":2,"stdout":"","stderr":"invalid delegate request\n","delegate_id":agent}
        stub=self.delegates_root/f"{agent}.json"
        self.log({"tool":"delegate","agent":agent,"instruction":instruction,"known_agent":stub.is_file()})
        if not stub.is_file():
            return {"returncode":2,"stdout":"","stderr":f"delegate: no agent named {agent!r} is available\n","delegate_id":agent}
        value=load_json(stub).get("return")
        return {"returncode":0,"stdout":(value if isinstance(value,str) else json.dumps(value))+"\n","stderr":"","delegate_id":agent}

    def call(self,name,args):
        handlers={"issues_locations":self.issues_locations,"issues_search":self.issues_search,"issues_show":self.issues_show,
                  "issues_create":self.issues_create,"issues_comment":self.issues_comment,"delegate":self.delegate}
        handler=handlers.get(name)
        return handler(args) if handler else {"returncode":2,"stdout":"","stderr":f"unsupported mediated tool {name!r}\n"}

TOOLS=[
 {"name":"issues_locations","description":"List qualification-owned issue stand-in locations and availability.","inputSchema":{"type":"object","properties":{},"additionalProperties":False}},
 {"name":"issues_search","description":"Search the qualification-owned issue stand-in.","inputSchema":{"type":"object","properties":{"query":{"type":"string"},"location":{"type":"string"}},"required":["query"],"additionalProperties":False}},
 {"name":"issues_show","description":"Read one qualification-owned stand-in issue.","inputSchema":{"type":"object","properties":{"issue_id":{"type":"string"}},"required":["issue_id"],"additionalProperties":False}},
 {"name":"issues_create","description":"Create an issue only in the qualification-owned stand-in store.","inputSchema":{"type":"object","properties":{"location":{"type":"string"},"title":{"type":"string"},"body":{"type":"string"},"labels":{"type":"array","items":{"type":"string"}}},"required":["location","title","body"],"additionalProperties":False}},
 {"name":"issues_comment","description":"Comment only on an issue in the qualification-owned stand-in store.","inputSchema":{"type":"object","properties":{"issue_id":{"type":"string"},"body":{"type":"string"}},"required":["issue_id","body"],"additionalProperties":False}},
 {"name":"delegate","description":"Call a scripted qualification-owned delegate stand-in; this cannot launch a live subagent.","inputSchema":{"type":"object","properties":{"agent":{"type":"string"},"instruction":{"type":"string"}},"required":["agent","instruction"],"additionalProperties":False}},
]

def write_message(message):
    sys.stdout.write(json.dumps(message,separators=(",",":"),sort_keys=True)+"\n"); sys.stdout.flush()

def rpc_error(request_id,code,message):
    return {"jsonrpc":"2.0","id":request_id,"error":{"code":code,"message":message}}

def tool_result(payload):
    return {"content":[{"type":"text","text":json.dumps(payload,sort_keys=True)}],"isError":int(payload.get("returncode",2))!=0}

def handle_message(store,message):
    if not isinstance(message,dict) or message.get("jsonrpc")!="2.0":
        return rpc_error(message.get("id") if isinstance(message,dict) else None,-32600,"Invalid Request")
    method,request_id,params=message.get("method"),message.get("id"),message.get("params") or {}
    if method=="initialize":
        return {"jsonrpc":"2.0","id":request_id,"result":{"protocolVersion":PROTOCOL_VERSION,"capabilities":{"tools":{"listChanged":False}},"serverInfo":{"name":SERVER_NAME,"version":SERVER_VERSION}}}
    if method in {"notifications/initialized","notifications/cancelled"}: return None
    if method=="ping": return {"jsonrpc":"2.0","id":request_id,"result":{}}
    if method=="tools/list": return {"jsonrpc":"2.0","id":request_id,"result":{"tools":TOOLS}}
    if method=="tools/call":
        if not isinstance(params,dict) or not isinstance(params.get("name"),str): return rpc_error(request_id,-32602,"Invalid tools/call params")
        args=params.get("arguments") or {}
        if not isinstance(args,dict): return rpc_error(request_id,-32602,"Tool arguments must be an object")
        return {"jsonrpc":"2.0","id":request_id,"result":tool_result(store.call(params["name"],args))}
    return None if request_id is None else rpc_error(request_id,-32601,f"Method not found: {method}")

def serve(store):
    for raw in sys.stdin.buffer:
        if len(raw)>MAX_LINE_BYTES:
            write_message(rpc_error(None,-32700,"MCP request exceeds maximum line size")); return 2
        if not raw.strip(): continue
        try: message=json.loads(raw)
        except json.JSONDecodeError:
            write_message(rpc_error(None,-32700,"Parse error")); continue
        try: response=handle_message(store,message)
        except Exception as exc:
            response=rpc_error(message.get("id") if isinstance(message,dict) else None,-32603,f"Internal mediator error: {exc}")
        if response is not None: write_message(response)
    return 0

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdio",action="store_true")
    parser.add_argument("--stub-root",type=Path,required=True)
    parser.add_argument("--side-effect-log",type=Path,required=True)
    parser.add_argument("--account",required=True)
    args=parser.parse_args()
    if not args.stdio: parser.error("only --stdio transport is supported")
    args.side_effect_log.parent.mkdir(parents=True,exist_ok=True); args.side_effect_log.touch()
    store=Store(args.stub_root,args.side_effect_log,args.account)
    os.environ.clear()
    return serve(store)

if __name__=="__main__":
    raise SystemExit(main())
