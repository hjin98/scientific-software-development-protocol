import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
SERVER=HERE/"stub_tools"/"mediator.py"

class StdioMcpMediatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.stub=self.root/"stub"
        self.issues=self.stub/"issues"; self.delegates=self.stub/"delegates"; self.issues.mkdir(parents=True); self.delegates.mkdir()
        (self.issues/"_config.json").write_text(json.dumps({"locations":{"local":"available","blocked":"unavailable"}}),encoding="utf-8")
        (self.issues/"local").mkdir()
        (self.issues/"local"/"I1.json").write_text(json.dumps({"title":"alpha","body":"needle","comments":[]}),encoding="utf-8")
        (self.delegates/"reviewer.json").write_text(json.dumps({"return":"delegate-ok"}),encoding="utf-8")
        self.log=self.root/"side-effects.jsonl"
        self.proc=subprocess.Popen([sys.executable,str(SERVER),"--stdio","--stub-root",str(self.stub),"--side-effect-log",str(self.log),"--account","agent"],
                                   stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        self.rpc(1,"initialize",{"protocolVersion":"2025-06-18"}); self.notify("notifications/initialized")
    def tearDown(self):
        if self.proc.stdin and not self.proc.stdin.closed: self.proc.stdin.close()
        self.proc.wait(timeout=5); self.tmp.cleanup()
    def send(self,value):
        assert self.proc.stdin is not None; self.proc.stdin.write(json.dumps(value)+"\n"); self.proc.stdin.flush()
    def read(self):
        assert self.proc.stdout is not None; return json.loads(self.proc.stdout.readline())
    def rpc(self,rid,method,params=None):
        self.send({"jsonrpc":"2.0","id":rid,"method":method,"params":params or {}}); row=self.read()
        self.assertEqual(row["id"],rid); self.assertNotIn("error",row); return row["result"]
    def notify(self,method,params=None): self.send({"jsonrpc":"2.0","method":method,"params":params or {}})
    def call(self,rid,name,args): return self.rpc(rid,"tools/call",{"name":name,"arguments":args})
    def payload(self,result): self.assertEqual(len(result["content"]),1); return json.loads(result["content"][0]["text"])
    def test_exact_tool_surface(self):
        tools=self.rpc(2,"tools/list")["tools"]
        self.assertEqual([x["name"] for x in tools],["issues_locations","issues_search","issues_show","issues_create","issues_comment","delegate"])
        self.assertTrue(all(x["inputSchema"].get("additionalProperties") is False for x in tools))
    def test_issue_mutation_is_mediated_and_versioned(self):
        shown=self.payload(self.call(3,"issues_show",{"issue_id":"I1"})); before=shown["before_version"]; self.assertEqual(before,shown["after_version"])
        changed=self.payload(self.call(4,"issues_comment",{"issue_id":"I1","body":"hello"})); self.assertEqual(changed["before_version"],before); self.assertNotEqual(changed["after_version"],before)
        rows=[json.loads(x) for x in self.log.read_text(encoding="utf-8").splitlines()]
        self.assertTrue(any(x.get("op")=="comment" and x.get("issue_id")=="I1" for x in rows))
    def test_delegate_is_scripted_standin(self):
        result=self.payload(self.call(5,"delegate",{"agent":"reviewer","instruction":"check"})); self.assertEqual(result["returncode"],0); self.assertIn("delegate-ok",result["stdout"])
        self.assertTrue(self.call(6,"delegate",{"agent":"missing","instruction":"check"})["isError"])
    def test_unknown_tool_fails_closed(self):
        result=self.call(7,"arbitrary_rpc",{}); self.assertTrue(result["isError"]); self.assertEqual(self.payload(result)["returncode"],2)

if __name__=="__main__":
    unittest.main()
