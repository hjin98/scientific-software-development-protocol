"""Real evidence-owner and isolated-pass regressions; synthetic material only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

EVAL = Path(__file__).resolve().parent.parent / 'eval'
sys.path.insert(0, str(EVAL))
import core70
import assessment_evidence as links
import assess70
import campaign_assess


class LinkRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.run = self.base / 'run'
        (self.run / 'final-tree').mkdir(parents=True)
        self.external = self.base / 'external'
        self.external.write_text('OUTSIDE_CANARY_DO_NOT_COPY')
        (self.run / 'final-tree/link').symlink_to(self.external)
        (self.run / 'final-tree/plain').write_text('ordinary content')
        (self.run / 'run-identity.json').write_text(json.dumps({'identity_sha256': 'identity'}))
        self.req = core70.Requirements(('final-tree', 'final-tree-symlinks.json'), (), (), 'a', 'o', 's')
        self.inventory()

    def inventory(self):
        rows = [{'path': p.relative_to(self.run / 'final-tree').as_posix(), 'target': os.readlink(p),
                 'resolves_inside_project': False} for p in (self.run / 'final-tree').rglob('*') if p.is_symlink()]
        (self.run / 'final-tree-symlinks.json').write_text(json.dumps({'schema': 1, 'symlinks': rows}))

    def legacy(self):
        # Reproduce the historical referent-accounting writer, only in this synthetic store.
        data = links.write_evidence_integrity(self.run, self.req)
        data.pop('symlink_accounting')
        rows = []
        for p in links._evidence_files(self.run, self.req):
            if p.is_file():
                rows.append({'path': p.relative_to(self.run).as_posix(), 'bytes': p.stat().st_size,
                             'sha256': core70.sha256_file(p)})
        data['files'] = rows
        (self.run / 'evidence-integrity.json').write_text(json.dumps(data))
        return (self.run / 'evidence-integrity.json').read_bytes()

    def errors(self):
        return links.validate_evidence_integrity(self.run, self.req)

    def test_new_manifest_link_text_round_trip_and_dangling_directory_links(self):
        (self.run / 'final-tree/dangling').symlink_to('/no/such/target')
        (self.run / 'final-tree/directory').symlink_to(self.base, target_is_directory=True)
        (self.run / 'final-tree/relative').symlink_to('plain')
        self.inventory()
        data = links.write_evidence_integrity(self.run, self.req)
        self.assertEqual(self.errors(), [])
        link = next(x for x in data['files'] if x['path'] == 'final-tree/link')
        self.assertEqual(link['sha256'], hashlib.sha256(os.fsencode(str(self.external))).hexdigest())
        self.external.write_text('REFERENT_CHANGED')
        self.assertEqual(self.errors(), [])

    def test_legacy_links_are_recovered_without_rewriting_or_reading_referent(self):
        (self.run / 'final-tree/dangling').symlink_to('/no/such/target')
        (self.run / 'final-tree/directory').symlink_to(self.base, target_is_directory=True)
        self.inventory()
        before = self.legacy()
        self.external.unlink()
        self.assertEqual(self.errors(), [])
        self.assertEqual((self.run / 'evidence-integrity.json').read_bytes(), before)

    def test_legacy_changed_removed_and_replaced_link_refused(self):
        for kind in ['changed', 'removed', 'file']:
            with self.subTest(kind=kind):
                link = self.run / 'final-tree/link'
                if link.exists() or link.is_symlink(): link.unlink()
                link.symlink_to(self.external)
                self.inventory(); self.legacy(); link.unlink()
                if kind == 'changed': link.symlink_to('/different/target')
                if kind == 'file': link.write_bytes(self.external.read_bytes())
                self.assertTrue(self.errors())

    def test_legacy_unrecorded_link_refused(self):
        self.legacy()
        (self.run / 'final-tree/extra').symlink_to(self.external)
        self.assertTrue(self.errors())

    def test_inventory_hash_and_absence_refused(self):
        self.legacy()
        p = self.run / 'final-tree-symlinks.json'
        p.write_text('{}')
        self.assertTrue(self.errors())
        p.unlink()
        self.assertTrue(self.errors())

    def test_duplicate_and_traversing_inventory_refused_even_when_hash_matches(self):
        for entries in [[{'path': 'link', 'target': str(self.external)}] * 2,
                        [{'path': '../outside', 'target': str(self.external)}],
                        [{'path': '/absolute', 'target': str(self.external)}]]:
            with self.subTest(entries=entries):
                p = self.run / 'final-tree-symlinks.json'
                p.write_text(json.dumps({'schema': 1, 'symlinks': entries}))
                self.legacy()
                self.assertTrue(self.errors())

    def test_ordinary_hash_and_symlink_ancestor_refused(self):
        self.legacy()
        (self.run / 'final-tree/plain').write_text('CHANGED')
        self.assertTrue(self.errors())
        self.assertIsNone(links._link_path(self.run, 'final-tree/link/child'))

    def test_new_link_to_file_and_target_change_refused(self):
        links.write_evidence_integrity(self.run, self.req)
        link = self.run / 'final-tree/link'; link.unlink(); link.symlink_to('/changed')
        self.assertTrue(self.errors())
        link.unlink(); link.write_text('ordinary')
        self.assertTrue(self.errors())

    def test_complete_reader_preserves_nonintegrity_failures_and_refuses_suffix_mismatch(self):
        self.legacy()
        identity = json.loads((self.run / 'run-identity.json').read_text())
        # An early core refusal must not be mistaken for its trailing integrity segment.
        errors = links.validate_complete_run(self.run, identity, self.req)
        self.assertTrue(any('suffix' in e for e in errors))
        req = core70.Requirements(self.req.artifacts, (), (), 'a' * 64, 'b' * 64, 'c' * 64)
        snapshot = core70.requirements_snapshot(req)
        identity['requirements'] = {'required_artifacts_sha256': req.artifact_manifest_digest,
                                    'required_oracles_sha256': req.oracle_manifest_digest,
                                    'expected_scoring_items_sha256': req.scoring_manifest_digest}
        (self.run / 'run-identity.json').write_text(json.dumps(identity))
        (self.run / 'requirements-snapshot.json').write_text(json.dumps(snapshot))
        (self.run / 'summary.json').write_text(json.dumps({'evidence_state': 'COMPLETE_ADMISSIBLE',
            'execution_ok': True, 'run_identity_sha256': 'WRONG_IDENTITY'}))
        (self.run / 'events.normalized.jsonl').write_text('')
        (self.run / 'normalization-map.json').write_text(json.dumps({'native_event_count': 0, 'entries': []}))
        self.req = req
        self.legacy()
        errors = links.validate_complete_run(self.run, identity, req)
        self.assertIn('run summary identity does not match current identity', errors)
        self.assertFalse(any('suffix' in e for e in errors))

    def test_legacy_ordinary_file_to_link_replacement_is_refused(self):
        self.legacy()
        plain = self.run / 'final-tree/plain'; plain.unlink(); plain.symlink_to(self.external)
        self.assertTrue(self.errors())

    def test_real_bundle_owner_emits_inert_blinded_descriptors_without_host_bytes(self):
        (self.run / 'final-tree/dir').symlink_to(self.base, target_is_directory=True)
        (self.run / 'final-tree/cycle').symlink_to('cycle')
        (self.run / 'final-tree/version').symlink_to('/SSDP-7.2.0/private')
        self.inventory(); self.legacy()
        self.assertEqual(self.errors(), [])
        keys = self.base / 'synthetic-keys'; keys.mkdir()
        root = self.base / 'bundle'; root.mkdir()
        assess70.prepare_bundle(self.run, keys, None, self.req, root)
        files = [p for p in root.rglob('*') if p.is_file()]
        self.assertFalse(any(p.is_symlink() for p in root.rglob('*')))
        self.assertFalse(any(b'OUTSIDE_CANARY' in p.read_bytes() for p in files))
        desc = json.loads((root / 'run/final-tree/link').read_text())
        self.assertTrue(desc['referent_not_copied'])
        self.assertNotIn('7.2.0', (root / 'run/final-tree/version').read_text())


class OutputRecovery(unittest.TestCase):
    def test_prompt_lists_metadata_without_answers_and_the_wrapper_attaches_measure_and_critical(self):
        spec = {'id': 'E::null_coverage.unowed', 'measure': 'null_coverage', 'critical': False,
                'branch': 'x', 'allowed_dispositions': ['pass', 'fail'], 'expected_answer': 'PRIVATE_NOT_IN_PROMPT'}
        req = core70.Requirements((), (), (spec,), 'a', 'o', 's')
        prompt = assess70.evaluator_prompt('E', req)
        self.assertNotIn('PRIVATE_NOT_IN_PROMPT', prompt)
        self.assertIn('Do not output measure or critical', prompt)
        result = {'episode': 'E', 'notes': '', 'dispositions': [{'item': spec['id'], 'result': 'pass', 'evidence': 'specific evidence'}]}
        self.assertEqual(assess70.validate_verdict(result, 'E', req), [])
        self.assertEqual(assess70.expand_rows(result['dispositions'], req),
                         [{'item': spec['id'], 'result': 'pass', 'evidence': 'specific evidence', 'measure': 'null_coverage', 'critical': False}])
        # strict: the old echo fields, other keys, unknown/duplicate/missing items, disallowed results and long evidence are all rejected, never normalized
        for bad in (dict(result['dispositions'][0], measure='null_coverage'), dict(result['dispositions'][0], critical=False),
                    dict(result['dispositions'][0], verdict='x'), {'item': spec['id'], 'result': 'pass'},
                    dict(result['dispositions'][0], result='maybe'), dict(result['dispositions'][0], item='E::other'),
                    dict(result['dispositions'][0], evidence='word ' * 41)):
            self.assertTrue(assess70.validate_verdict(dict(result, dispositions=[bad]), 'E', req), bad)
        self.assertTrue(assess70.validate_verdict(dict(result, dispositions=result['dispositions'] * 2), 'E', req))
        self.assertTrue(assess70.validate_verdict(dict(result, dispositions=[]), 'E', req))
        for odd in ('not-a-dict', None, 7, [spec['id']], dict(result['dispositions'][0], item=7), dict(result['dispositions'][0], item=['E::null_coverage.unowed']),
                    dict(result['dispositions'][0], item={'x': 1})):                  # malformed rows are rejected, never repaired by expand_rows
            self.assertTrue(assess70.validate_verdict(dict(result, dispositions=[odd]), 'E', req), odd)
        self.assertEqual(assess70.expand_rows('x', req), 'x')

    def test_separate_pass_collection_does_not_fall_back_to_original_assessments(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = Path(tmp); d = w / 'runs/main-c01/E-p72-r0'; d.mkdir(parents=True)
            (d / 'summary.json').write_text(json.dumps({'evidence_state': 'COMPLETE_ADMISSIBLE'}))
            old = json.dumps({'assessment_status': 'VALID', 'dispositions': [{'item': 'E::item', 'result': 'pass'}]})
            (d / 'assessment.json').write_text(old)
            a = argparse.Namespace(work=w, panels=['main'], assessment_root=w / 'evaluations/recovery-1', out=w/'disp.json')
            self.assertEqual(campaign_assess.cmd_collect(a), 4)
            output = campaign_assess.assessment_dir(d, a); output.mkdir(parents=True)
            (output / 'assessment.json').write_text(json.dumps({'assessment_status': 'VALID', 'dispositions': [{'item': 'E::item', 'result': 'fail'}]}))
            self.assertEqual(campaign_assess.cmd_collect(a), 0)
            self.assertEqual(json.loads(a.out.read_text()), {'E-p72-r0::item': 'fail'})
            self.assertEqual((d / 'assessment.json').read_text(), old)
            a.assessment_root = w / 'runs'
            with self.assertRaises(ValueError): campaign_assess.assessment_dir(d, a)
