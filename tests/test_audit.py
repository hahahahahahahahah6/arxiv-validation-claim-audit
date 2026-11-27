import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from arxiv_validation_claim_audit.audit import audit, claims, evidence, prose
from arxiv_validation_claim_audit.phrases import GENERIC, YES, NO

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        for phrase in YES:
            with self.subTest(phrase=phrase):
                self.assertEqual(claims(phrase), (True, False))
        for phrase in NO:
            with self.subTest(phrase=phrase):
                self.assertEqual(claims(phrase), (False, True))
        self.assertEqual(claims('documented-arxiv-validation-claim-false'), (True, False))
        self.assertEqual(claims('xvalidate arxivz'), (False, False))
        self.assertEqual(claims(prose('```\nvalidate arxiv\n```')), (False, False))

    def test_library_routes(self):
        for name in ('is_arxiv', 'is_arxiv_post_2007', 'is_arxiv_pre_2007'):
            for source in ('import idutils\nidutils.' + name + '(x)', 'import idutils as iu\niu.' + name + '(x)', 'from idutils import ' + name + ' as f\nf(x)'):
                with self.subTest(source=source):
                    self.assertTrue(evidence(source))

    def test_generic_routes(self):
        for name in GENERIC:
            for source in ('obj.' + name + '(x)', 'from other import ' + name + ' as f\nf(x)', 'obj = make()\nobj.' + name + '(x)'):
                with self.subTest(source=source):
                    self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import idutils', 'is_arxiv(x)', 'obj.is_arxiv(x)', 'validate_arxiv(x)', '"validate arxiv"', 'obj.validate_arxiv', 'def bad(:', 'import subprocess\nsubprocess.run(["checker"])', 'len(x)', '"." in x', 'x.startswith("arxiv:")', 'import re\nre.match("x", x)', 'import validators\nvalidators.url(x)', 'import stdnum\nstdnum.validate(x)']
        cases += ['import arxiv\narxiv.' + n + '(x)' for n in ('Search', 'Client', 'Result')]
        cases += ['import idutils\nidutils.' + n + '(x)' for n in ('normalize_arxiv', 'to_url', 'detect_identifier_schemes', 'is_doi', 'is_handle', 'is_ark', 'is_urn', 'is_pmid', 'is_pmcid', 'is_istc', 'is_cstr', 'is_ror', 'is_openalex', 'is_viaf', 'is_wikidata', 'is_gnd', 'is_hal', 'is_swh', 'is_rrid', 'is_ean', 'is_ean13', 'is_ean8', 'is_email', 'is_url', 'is_orcid', 'is_isni', 'is_isbn', 'is_isbn10', 'is_isbn13', 'is_issn')]
        cases += ['import idutils\nidutils.' + n + '.' + op + '(x)' for n in ('arxiv_post_2007_regexp', 'arxiv_pre_2007_regexp', 'arxiv_post_2007_with_class_regexp') for op in ('match', 'search')]
        cases += ['import idutils as iu\niu = 1\niu.is_arxiv(x)', 'import idutils as iu\nwith x as iu:\n iu.is_arxiv(x)', 'def validate_arxiv(x): pass\nobj.validate_arxiv(x)', 'from idutils import is_arxiv as f\nf = 1\nf(x)']
        for source in cases:
            with self.subTest(source=source):
                self.assertFalse(evidence(source))

    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'README.md').write_text('validate arxiv')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')
            (p/'tests').mkdir()
            (p/'tests/test_x.py').write_text('import idutils\nidutils.is_arxiv(x)')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'MEDIUM')
            (p/'x.py').write_text('import idutils\nidutils.is_arxiv(x)')
            self.assertEqual(audit(p)['findings'], [])
            (p/'README.md').write_text('does not validate arxiv')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'README.md').write_text('validate arxiv')
            cmd = [sys.executable, '-m', 'arxiv_validation_claim_audit', 'audit', d, '--json']
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(len(json.loads(result.stdout)['findings']), 1)
            self.assertEqual(subprocess.run(cmd + ['--ignore', 'README.md'], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run([sys.executable, '-m', 'arxiv_validation_claim_audit', 'audit', '/not/a/path'], capture_output=True).returncode, 1)

if __name__ == '__main__':
    unittest.main()
