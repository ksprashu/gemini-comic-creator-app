import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import logic
except ImportError:
    logic = None

class TestImageGeneration(unittest.TestCase):
    def test_logic_module_exists(self):
        self.assertIsNotNone(logic, "logic module should exist")

    @patch('logic.genai.Client')
    def test_generate_image_calls_api(self, mock_client_cls):
        """Verify generate_image calls the Gemini API with correct parameters."""
        if not logic:
            self.fail("logic module missing")
        
        # Setup mock
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_image = MagicMock()
        mock_response.generated_images = [MagicMock(image=mock_image)]
        mock_client.models.generate_images.return_value = mock_response
        
        # Call function
        prompt = "A cyberpunk cat"
        result = logic.generate_image(prompt)
        
        # Assertions
        mock_client.models.generate_images.assert_called_once()
        call_args = mock_client.models.generate_images.call_args
        self.assertEqual(call_args.kwargs['model'], 'gemini-3-pro-image-preview')
        self.assertEqual(call_args.kwargs['prompt'], prompt)
        self.assertEqual(result, mock_image)

if __name__ == '__main__':
    unittest.main()