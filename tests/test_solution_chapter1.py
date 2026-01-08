import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the solution module
from solutions.chapter1 import logic

class TestSolutionChapter1(unittest.TestCase):
    @patch('solutions.chapter1.logic.genai.Client')
    def test_generate_image_calls_api(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_image = MagicMock()
        mock_response.generated_images = [MagicMock(image=mock_image)]
        mock_client.models.generate_images.return_value = mock_response
        
        prompt = "A cyberpunk cat"
        result = logic.generate_image(prompt)
        
        mock_client.models.generate_images.assert_called_once()
        self.assertEqual(result, mock_image)

if __name__ == '__main__':
    unittest.main()