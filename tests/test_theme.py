import sys
import os
import unittest
import gradio as gr

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import theme

class TestTheme(unittest.TestCase):
    def test_theme_instance(self):
        """Verify that the theme function returns a Theme object."""
        # Gradio themes inherit from Base
        self.assertIsInstance(theme.get_theme(), gr.themes.Base)

if __name__ == '__main__':
    unittest.main()
