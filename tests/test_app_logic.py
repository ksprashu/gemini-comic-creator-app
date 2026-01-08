import sys
import os
import unittest
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app

class TestAppLogic(unittest.TestCase):
    def test_run_diagnostics_failure(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "PLACEHOLDER_KEY"}):
            msg = app.run_diagnostics()
            self.assertIn("FAILED", msg)

    def test_run_diagnostics_success(self):
        # AIza + 35 chars = 39 chars total
        valid_key = "AIza" + "x" * 35
        with patch.dict(os.environ, {"GOOGLE_API_KEY": valid_key}):
            msg = app.run_diagnostics()
            self.assertIn("OPTIMAL", msg)

    def test_check_unlock_success(self):
        log = "SYSTEM_CHECK: OPTIMAL..."
        u1, u2, u3 = app.check_unlock(log)
        # Gradio update objects are dictionaries in recent versions or objects
        # accessing them like dicts works for `visible` etc usually.
        self.assertEqual(u1['label'], "CHAPTER 1: INK & FUR")
        self.assertEqual(u1['interactive'], True)
        self.assertEqual(u2['visible'], True)
        self.assertEqual(u3['visible'], False)

    def test_check_unlock_failure(self):
        log = "SYSTEM_CHECK: FAILED..."
        u1, u2, u3 = app.check_unlock(log)
        # Empty update usually has no changes.
        # Verify it doesn't have label change
        self.assertTrue(u1 == app.gr.update()) 

if __name__ == '__main__':
    unittest.main()
