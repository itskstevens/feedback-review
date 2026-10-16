"""Unit tests for scripts/build_page.py. Run: python3 -m unittest discover tests"""
import copy
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "feedback-review", "scripts"))
import build_page  # noqa: E402

SAMPLE = json.load(open(os.path.join(ROOT, "examples", "sample-data.json"), encoding="utf-8"))


class ValidateTests(unittest.TestCase):
    def test_sample_is_valid(self):
        errs, _ = build_page.validate(SAMPLE)
        self.assertEqual(errs, [])

    def test_old_must_match_once(self):
        d = copy.deepcopy(SAMPLE)
        d["edits"].append({"id": "e99", "us": "US-03", "op": "ac_change", "fb": ["F1"], "old": "not in the story", "txt": "x"})
        errs, _ = build_page.validate(d)
        self.assertTrue(any("exactly once" in e for e in errs))

    def test_txt_already_present(self):
        d = copy.deepcopy(SAMPLE)
        d["edits"].append({"id": "e99", "us": "US-03", "op": "ac_add", "fb": ["F1"], "txt": "I can see which of my steps are overdue."})
        errs, _ = build_page.validate(d)
        self.assertTrue(any("already appears" in e for e in errs))

    def test_unknown_feedback(self):
        d = copy.deepcopy(SAMPLE)
        d["edits"][0]["fb"] = ["F42"]
        errs, _ = build_page.validate(d)
        self.assertTrue(any("unknown feedback" in e for e in errs))

    def test_missing_session_field(self):
        d = copy.deepcopy(SAMPLE)
        del d["session"]["futureMilestone"]
        errs, _ = build_page.validate(d)
        self.assertTrue(any("futureMilestone" in e for e in errs))

    def test_dash_is_a_warning(self):
        d = copy.deepcopy(SAMPLE)
        d["feedback"][0]["summary"] = "Filters — lots of them."
        errs, warns = build_page.validate(d)
        self.assertEqual(errs, [])
        self.assertTrue(any("dash" in w for w in warns))

    def test_build_escapes_script_close(self):
        d = copy.deepcopy(SAMPLE)
        d["feedback"][0]["t"] = "Pasted </script> by accident"
        html = build_page.build(d, build_page.DEFAULT_TEMPLATE)
        self.assertNotIn("Pasted </script>", html)
        self.assertNotIn("__AUDIT_DATA__", html)


if __name__ == "__main__":
    unittest.main()
