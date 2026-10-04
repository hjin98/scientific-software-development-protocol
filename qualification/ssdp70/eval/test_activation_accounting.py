"""Non-custody implementation discriminators through the real OMP/observer/harness/core/scorer.

The external model provider alone is a local stand-in. No qualification/admission is performed.
"""
import copy
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import core70
import harness70
import observer70
import omp_rig
import batch_assess70
from adapters import omp


class FamilyAndScope(unittest.TestCase):
    def test_transform_is_exact_decoded_content_and_rejects_wrong_root_truncation_late_and_auxiliary(self):
        skill = b'---\nname: software-design\ndescription: Never select for arithmetic.\n---\n# Canary\nTOKEN\n'
        spec = {"transform": observer70.OMP_RPC_TRANSFORM, "root": "software-design", "prompt": "2+2?",
                "directory": "/opt/ssdp/skills/software-design", "mechanism": "runtime-command",
                "skill_b64": __import__('base64').b64encode(skill).decode(),
                "installed_skill_sha256": core70.stable_json_sha256("skill"), "installed_skill_bytes": len(skill),
                "runtime_input_sha256": "b" * 64}
        segment = observer70.delivery_segment(skill, spec['root'], spec['prompt'], spec['directory'], spec['transform'])
        def body(text): return json.dumps({'messages':[{'role':'system','content':'catalog'}, {'role':'user','content':[{'type':'text','text':'reminder'},{'type':'text','text':text}]}]}).encode()
        self.assertTrue(observer70.delivery_proof(body(segment), spec)['delivered'])
        for text in ('', segment[:-1], segment.replace('software-design','software-implementation'), '/skill:software-design 2+2?'):
            self.assertFalse(observer70.delivery_proof(body(text), spec)['delivered'])
        wrong = json.loads(body(segment)); wrong['messages'][1]['role']='assistant'
        self.assertFalse(observer70.delivery_proof(json.dumps(wrong).encode(),spec)['delivered'])
        # Every allowed POST is conversation; an auxiliary marker cannot hide missing skill text.
        self.assertEqual(spec['transform']['classification']['auxiliary_post_requests'], [])

    def test_malformed_family_and_missing_map_fail_closed(self):
        self.assertTrue(core70.validate_family({}))
        self.assertTrue(core70.campaign_manifest_errors({'purpose':'qualification','scope_id':'x','runs':[]}))

    def test_missing_integrity_result_and_unexpected_result_block(self):
        expected = {'evidence_state':'INADMISSIBLE','criteria':{'deterministic activation':'FAIL'},'qualification_outcome':'NOT_EVALUATED'}
        self.assertEqual(core70.integrity_assessment(expected, expected)['integrity_outcome'],'PASS')
        actual = copy.deepcopy(expected); actual['criteria']['deterministic activation']='PASS'
        self.assertEqual(core70.integrity_assessment(actual,expected)['integrity_outcome'],'FAIL')
        self.assertEqual(core70.integrity_assessment({}, expected)['integrity_outcome'],'FAIL')


@unittest.skipIf(bool(omp_rig.prerequisites()), str(omp_rig.prerequisites()))
class RealActivationPath(unittest.TestCase):
    def realize(self, fault=None, mechanism='runtime-command', root='software-implementation', scenario=None, canary=False, no_delegate=False, claims=None, local_expected=None):
        rig = omp_rig.Rig(Path('/tmp'), entry='pinned:'+root, timeout_s=45, claims=claims)
        if canary:
            package = rig.root / "canary-package"
            shutil.copytree(omp_rig.DIST_SKILLS, package)
            (package / root / "SKILL.md").write_text(
                "---\nname: " + root + "\ndescription: Never select this skill for any user task; synthetic delivery canary only.\n---\n# Delivery canary\nSSDP70_CANARY_612033af\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n")
            rig.arm = {**rig.arm, "skills_path": str(package), "dist_tree_sha256": core70.sha256_tree(package)}
            omp_rig.write_json(rig.arms_manifest, {"schema": 1, "arms": [rig.arm]})
            rig.arms_manifest_sha = core70.sha256_file(rig.arms_manifest)
        original_run_identity = harness70.run_identity
        manifest_holder = {}
        original_profile = rig.profile
        def profile(upstream, **kwargs):
            p = original_profile(upstream, **kwargs)
            p.update(runtime_mode='rpc',activation_mechanism=mechanism,delivery_transform=observer70.OMP_RPC_TRANSFORM,
                     runtime_input_template=omp.input_template(mechanism))
            if canary:
                p['native_tools'] = []
                p['mcp_servers'] = []
            elif no_delegate:
                p['native_tools'] = [name for name in p['native_tools'] if 'delegate' not in name]
                p['mcp_servers'][0]['tools'] = [name for name in p['mcp_servers'][0]['tools'] if 'delegate' not in name]
                # The adapter derives the exact tool map from this declared subset.
            return p
        rig.profile = profile
        def identity(**kwargs):
            bundle = kwargs['profile_bundle']; req = kwargs['requirements']; arm = kwargs['arm']
            expected={'evidence_state':'INADMISSIBLE' if fault or canary else 'COMPLETE_ADMISSIBLE',
                'criteria':{'harness/admissibility':'FAIL' if fault or canary else 'PASS','deterministic activation':'FAIL' if fault else 'PASS'},
                'qualification_outcome':'NOT_EVALUATED' if fault or canary else 'PASS'}
            if local_expected is not None:
                expected = local_expected
            manifest={'purpose':'oracle-integrity','scope_id':'implementation:'+rig.root.name,'runs':[{
                'id':'E1-p70-r0','profile_key_sha256':bundle.profile_key_sha256,'entry_stratum':'deterministic',
                'subject':{'commit':arm['commit'],'package_sha256':arm['dist_tree_sha256']},
                'scoring_manifest_sha256':req.scoring_manifest_digest,'fault':fault or 'known-good','expected':expected}]}
            manifest_holder['manifest']=manifest
            kwargs['episode']={**kwargs['episode'],'accounting_manifest':manifest}
            return original_run_identity(**kwargs)
        # This changes only pre-launch manifest construction; real run identity owner still executes.
        harness70.run_identity = identity
        try:
            summary = rig.run(scenario or {'steps':[{'text':'CANARY-DEVELOPMENT'}]})
        finally:
            harness70.run_identity = original_run_identity
        out = Path(summary['_out']); identity = core70.load_json(out/'run-identity.json')
        requirements=core70.load_requirements(rig.req_root,'E1')
        dispositions=None if fault else [{'item':'i1','measure':'critical','critical':True,'result':'pass','evidence':'The collected deterministic oracle exited 0.'}]
        assessment=core70.production_assessment(summary,identity,requirements,dispositions)
        omp_rig.write_json(out/'assessment.json',assessment)
        # Production scorer consumes actual retained files, not booleans supplied to a substitute.
        rootdir=rig.root/'aggregation'; rootdir.mkdir()
        os.symlink(out,rootdir/'E1-p70-r0',target_is_directory=True)
        aggregate=batch_assess70.aggregate_assessments(rootdir,manifest_holder['manifest'])
        omp_rig.write_json(rig.root/'production-integrity-assessment.json',aggregate)
        return summary,aggregate,identity,rig

    def test_known_good_each_declared_root_and_honestly_labelled_injection(self):
        for root in sorted(omp.SSDP_SKILLS):
            with self.subTest(root=root):
                summary,aggregate,identity,rig=self.realize(root=root)
                self.assertEqual(summary['evidence_state'],'COMPLETE_ADMISSIBLE', summary.get('evidence_state_reasons'))
                self.assertTrue(summary['activation']['delivered'])
                self.assertEqual(aggregate['integrity_outcome'],'PASS',aggregate)
                self.assertEqual(aggregate['total_runs'],0)
                self.assertEqual(aggregate['arms'],{})
                self.assertEqual(summary['activation']['installed_skill_bytes'],summary['active_ssdp_bytes'])
        summary,aggregate,_,_=self.realize(mechanism='harness-injection')
        self.assertEqual(summary['evidence_state'],'COMPLETE_ADMISSIBLE',summary.get('evidence_state_reasons'))
        self.assertEqual(aggregate['integrity_outcome'],'PASS')

    def test_all_broken_probes_keep_local_failure_and_only_outer_integrity_passes(self):
        for fault in sorted(omp.INTEGRITY_FAULTS):
            with self.subTest(fault=fault):
                scenario={'steps':[{'tool_calls':[{'name':'read','arguments':{'path':'skill://software-implementation'}}]},{'text':'after model read'}]} if fault=='instructed-read' else None
                summary,aggregate,identity,rig=self.realize(fault=fault,scenario=scenario)
                self.assertEqual(summary['evidence_state'],'INADMISSIBLE',summary)
                self.assertEqual(summary['criteria']['deterministic activation'],'FAIL')
                self.assertEqual(aggregate['integrity_outcome'],'PASS',aggregate)
                self.assertEqual(aggregate['total_runs'],0)
                self.assertEqual(aggregate['arms'],{})
                changed=copy.deepcopy(identity); changed['accounting']['purpose']='qualification'
                self.assertTrue(core70.validate_accounting_identity(changed))
                self.assertFalse(core70.cache_valid(Path(summary['_out']),changed,core70.load_requirements(rig.req_root,'E1')))
                changed_summary=copy.deepcopy(summary); changed_summary['accounting']=dict(changed['accounting'])
                with self.assertRaises(core70.ContractError):
                    core70.production_assessment(changed_summary,identity,core70.load_requirements(rig.req_root,'E1'))

    def test_canary_without_tools_and_burden_without_delegate_use_real_runtime(self):
        summary, aggregate, identity, rig = self.realize(canary=True)
        # OMP omits its catalog without tools: preserve full-profile inadmissibility.
        # The positive canary claim is request-0 delivery, not runner admission.
        self.assertEqual(summary['evidence_state'], 'INADMISSIBLE', summary.get('evidence_state_reasons'))
        self.assertEqual(aggregate['integrity_outcome'], 'PASS', aggregate)
        self.assertEqual(summary['runtime_observation']['tools'], [])
        self.assertTrue(summary['activation']['delivered'])
        summary, aggregate, identity, rig = self.realize(no_delegate=True)
        self.assertEqual(summary['evidence_state'], 'COMPLETE_ADMISSIBLE', summary.get('evidence_state_reasons'))
        self.assertFalse(any('delegate' in tool for tool in summary['runtime_observation']['tools']))
        self.assertEqual(aggregate['integrity_outcome'], 'PASS', aggregate)

    OWNER_REL = 'software-implementation/references/scientific-inspectability-and-initiative.md'
    OWNER_PATH = '/opt/ssdp/skills/' + OWNER_REL

    def process_case(self, command=None, tool=None):
        call = tool or {'name': 'bash', 'arguments': {'command': command}}
        scenario = {'steps': [{'tool_calls': [call]}, {'text': 'process observation discriminator'}]}
        return self.realize(scenario=scenario, claims=['active-byte burden', 'owner-read'])

    def test_process_read_with_supplied_content_is_exactly_accounted(self):
        """Real OMP model reads the owner through `bash`; the supervisor ledger plus observer-seen output account it."""
        root_bytes = (omp_rig.DIST_SKILLS / 'software-implementation' / 'SKILL.md').stat().st_size
        owner_bytes = (omp_rig.DIST_SKILLS / self.OWNER_REL).stat().st_size
        for name, command, bytes_counted in (
                ('cat', f'cat {self.OWNER_PATH}', owner_bytes),
                ('head', f'head -n 40 {self.OWNER_PATH}', owner_bytes),      # partial supply counts the file once
                ('grep lines', f"grep -n 'owner' {self.OWNER_PATH}", owner_bytes)):
            with self.subTest(name):
                summary, aggregate, identity, rig = self.process_case(command)
                self.assertEqual(summary['evidence_state'], 'COMPLETE_ADMISSIBLE', summary.get('evidence_state_reasons'))
                observation = summary['resource_observation']
                self.assertTrue(observation['exact'], observation)
                self.assertEqual(observation['mechanism'], 'inotify-inode-marks')
                self.assertEqual(sorted(observation['accounting']['opened_pre_request0']),
                                 sorted(f'{r}/SKILL.md' for r in omp.SSDP_SKILLS))
                self.assertEqual(summary['active_ssdp_bytes'], root_bytes + bytes_counted)
                self.assertTrue(summary['owner_read_sequences'], summary['owner_read_sequences'])
                self.assertEqual(aggregate['integrity_outcome'], 'PASS', aggregate)

    def test_process_access_without_shown_content_is_inadmissible_for_burden_and_owner_claims(self):
        """Opened package files whose content cannot be shown to have reached the model are named, never lower-bounded."""
        expected = {'evidence_state': 'INADMISSIBLE',
                    'criteria': {'harness/admissibility': 'FAIL', 'deterministic activation': 'PASS'},
                    'qualification_outcome': 'NOT_EVALUATED'}
        for name, call in (
                ('count', {'name': 'bash', 'arguments': {'command': f'wc -l {self.OWNER_PATH}'}}),
                ('transformed', {'name': 'bash', 'arguments': {'command': f'base64 {self.OWNER_PATH} | head -c 200'}}),
                ('native grep over package', {'name': 'grep', 'arguments': {'pattern': 'owner', 'path': '/opt/ssdp/skills/software-implementation/references'}})):
            with self.subTest(name):
                scenario = {'steps': [{'tool_calls': [call]}, {'text': 'process observation discriminator'}]}
                summary, aggregate, identity, rig = self.realize(scenario=scenario, claims=['active-byte burden', 'owner-read'],
                                                                 local_expected=expected)
                self.assertEqual(summary['evidence_state'], 'INADMISSIBLE', summary.get('evidence_state_reasons'))
                self.assertTrue(summary['activation']['delivered'])
                observation = summary['resource_observation']
                self.assertFalse(observation['exact'], observation)
                self.assertIn('package-access observation is not exact', observation['reason'])
                self.assertIn(self.OWNER_REL if name != 'native grep over package' else 'software-implementation/references/',
                              observation['reason'])
                self.assertIsNone(summary['active_ssdp_bytes'])
                self.assertIsNone(summary['owner_read_sequences'])
                self.assertEqual(aggregate['integrity_outcome'], 'PASS', aggregate)

    def test_qualification_scoped_integrity_campaign_keeps_failure_after_good_repeat(self):
        """Real campaign aggregation; outer suite purpose remains integrity throughout."""
        rig = omp_rig.Rig(Path('/tmp'), entry='pinned:software-implementation', timeout_s=45, max_turns=60)
        original_profile = rig.profile
        original_identity = harness70.run_identity
        original_episode = harness70.run_episode
        holder = {}

        def profile(upstream, **kwargs):
            p = original_profile(upstream, **kwargs)
            # Synthetic provider advertises the campaign model id to exercise identity
            # binding. It is a stand-in, never evidence about that model's behavior.
            p['containment_policy']['provider_route'].update(provider_id='deepinfra', model_id='zai-org/GLM-5.3-Flash')
            p.update(agent_model='deepinfra/zai-org/GLM-5.3-Flash', runtime_mode='rpc',
                     activation_mechanism='runtime-command', delivery_transform=observer70.OMP_RPC_TRANSFORM,
                     runtime_input_template=omp.input_template('runtime-command'))
            return p
        rig.profile = profile

        def make_identity(**kwargs):
            base = kwargs['profile_bundle'].profile_key
            if 'manifest' not in holder:
                keys = {}
                panels = {}
                for panel in ('main','burden','ordinary','routing'):
                    key = copy.deepcopy(base)
                    key['budgets']['max_turns'] = 3 if panel=='ordinary' else 8 if panel=='routing' else 60
                    if panel=='ordinary':
                        key['activation_mechanism']='ordinary-read'
                        key['runtime_input_template']=omp.input_template('ordinary-read')
                    if panel=='burden':
                        key['native_tools']=[t for t in key['native_tools'] if 'delegate' not in t]
                        key['mcp_servers'][0]['tools']=[t for t in key['mcp_servers'][0]['tools'] if 'delegate' not in t]
                    digest=core70.stable_json_sha256(key); keys[digest]=key
                    panels[panel]={'key':digest,'max_turns':key['budgets']['max_turns']}
                for panel in ('sentinels','versioning','r2'):
                    panels[panel]=copy.deepcopy(panels['main'])
                ordered=list(keys); ordinary=panels['ordinary']['key']
                deterministic=[key for key in ordered if key!=ordinary]
                mapping={part: ordered if row[1]=='all' else deterministic if row[1]=='deterministic' else [panels[row[1]]['key']]
                         for part,row in core70.CAMPAIGN_PARTS.items()}
                family={'serialization':core70.FAMILY_SERIALIZATION,'hash_algorithm':'sha256','ordered_keys':ordered,
                        'profile_keys':keys,'panels':panels,'criterion_to_keys':mapping,
                        'aggregation':{'owner_false_activation':'pool-all-keys','predicate_false_firing':'pool-all-keys','failures':'never-remove'}}
                family['family_id']=core70.family_id(family)
                self.assertEqual(core70.validate_family(family),[])
                declaration={'profile_key_sha256':kwargs['profile_bundle'].profile_key_sha256,'entry_stratum':'deterministic',
                             'subject':{'commit':kwargs['arm']['commit'],'package_sha256':kwargs['arm']['dist_tree_sha256']},
                             'scoring_manifest_sha256':kwargs['requirements'].scoring_manifest_digest}
                suite={'purpose':'oracle-integrity','scope_id':rig.root.name,
                       'test':'campaign delivery failure followed by delivered repeat still fails activation'}
                holder['suite']=suite
                holder['manifest']={'purpose':'qualification','scope_id':'test-campaign:'+rig.root.name,
                    'integrity_test_campaign':{'purpose':'oracle-integrity','suite_sha256':core70.stable_json_sha256(suite)},
                    'family':family,'family_record_sha256':core70.stable_json_sha256(family),
                    'offered_profiles':ordered,'prior_campaigns':[],'candidate_arm':'p70','comparator_arm':'p66',
                    'runs':[{**declaration,'id':'E1-p70-r0','fault':'withheld'}, {**declaration,'id':'E1-p70-r1'}]}
                omp_rig.write_json(rig.root/'integrity-suite-declaration.json',suite)
                omp_rig.write_json(rig.root/'test-campaign-manifest.json',holder['manifest'])
                malformed=copy.deepcopy(family); del malformed['criterion_to_keys']['critical']
                holder['bad_map']=malformed
            kwargs['episode']={**kwargs['episode'],'accounting_manifest':holder['manifest']}
            return original_identity(**kwargs)

        def episodes(**kwargs):
            first=original_episode(**kwargs)
            next_args={key:kwargs[key] for key in ('corpus','episode','arm','arms_manifest_sha256','dist','profile_bundle','profile_path',
                'capability_path','requirements','requirements_root','adapter_module','oracles','mode','admission','pair_order')}
            second_identity=make_identity(**next_args,rep=1)
            second=original_episode(**next_args,identity=second_identity,out=rig.root/'repeat')
            holder['runs']=[(kwargs['out'],first),(rig.root/'repeat',second)]
            return first
        harness70.run_identity=make_identity
        harness70.run_episode=episodes
        try:
            rig.run({'steps':[{'text':'withheld command campaign discriminator'},{'text':'delivered repeat'}]})
        finally:
            harness70.run_identity=original_identity
            harness70.run_episode=original_episode
        aggregate_root=rig.root/'campaign-aggregation'; aggregate_root.mkdir()
        requirements=core70.load_requirements(rig.req_root,'E1')
        for rep,(out,summary) in enumerate(holder['runs']):
            identity=core70.load_json(out/'run-identity.json')
            disposition=None if rep==0 else [{'item':'i1','measure':'critical','critical':True,'result':'pass','evidence':'Collected development oracle exit 0.'}]
            omp_rig.write_json(out/'assessment.json',core70.production_assessment(summary,identity,requirements,disposition))
            os.symlink(out,aggregate_root/f'E1-p70-r{rep}',target_is_directory=True)
        actual=batch_assess70.aggregate_assessments(aggregate_root,holder['manifest'])
        omp_rig.write_json(rig.root/'actual-test-campaign-assessment.json',actual)
        checks={'purpose':'oracle-integrity','suite_sha256':core70.stable_json_sha256(holder['suite']),
                'actual_campaign_activation':actual['criteria']['deterministic activation'],
                'actual_campaign_runs':actual['total_runs'], 'actual_repeat_activation':holder['runs'][1][1]['criteria']['deterministic activation'],
                'qualification_evidence_supplied':False}
        self.assertEqual(actual['criteria']['deterministic activation'],'FAIL')
        self.assertEqual(actual['total_runs'],2)
        self.assertEqual(holder['runs'][1][1]['criteria']['deterministic activation'],'PASS')
        self.assertTrue(all(row['qualification_outcome']!='PASS' for row in actual['profiles'].values()))
        # Real consumer rejects cross-scope evidence, even with unchanged runtime bytes.
        outer=copy.deepcopy(holder['manifest']); outer['purpose']='oracle-integrity'
        for row in outer['runs']:
            row.update(fault='known-good',expected={'evidence_state':'COMPLETE_ADMISSIBLE','criteria':{},'qualification_outcome':'PASS'})
        with self.assertRaises(core70.ContractError) as rejection:
            batch_assess70.aggregate_assessments(aggregate_root,outer)
        checks['cross_scope_rejection']=str(rejection.exception)
        bad=copy.deepcopy(holder['manifest']); bad['family']=holder['bad_map']
        bad['family_record_sha256']=core70.stable_json_sha256(bad['family'])
        with self.assertRaises(core70.ContractError) as rejection:
            batch_assess70.aggregate_assessments(aggregate_root,bad)
        checks['missing_map_rejection']=str(rejection.exception)
        checks['integrity_outcome']='PASS'
        omp_rig.write_json(rig.root/'outer-test-campaign-integrity-assessment.json',checks)
