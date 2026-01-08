import sys
import os
import unittest
from gradio import Blocks

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app

class TestAppStructure(unittest.TestCase):
    def test_app_is_blocks(self):
        """Verify that the app object is a Gradio Blocks instance."""
        self.assertIsInstance(app.app, Blocks)
    
    def test_title_contains_gemini(self):
        """Verify the title contains 'Gemini Comic Creator'."""
        # Note: Accessing title from Blocks object might depend on Gradio version internals
        # But we can check if it was passed in construction if we mock it, 
        # or just check the title attribute if accessible.
        self.assertTrue("Gemini Comic Creator" in app.app.title)

if __name__ == '__main__':
    unittest.main()
