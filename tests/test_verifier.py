import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import verifier

class TestVerifier(unittest.TestCase):
    @patch('verifier.genai.Client')
    def test_verify_image_success(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "YES" 
        mock_client.models.generate_content.return_value = mock_response
        
        mock_image = MagicMock()
        result, message = verifier.verify_image(mock_image)
        
        self.assertTrue(result)
        self.assertIn("Systems online", message)

    @patch('verifier.genai.Client')
    def test_verify_image_failure(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        mock_response.text = "NO" 
        mock_client.models.generate_content.return_value = mock_response
        
        mock_image = MagicMock()
        result, message = verifier.verify_image(mock_image)
        
        self.assertFalse(result)
        self.assertIn("Protocol Mismatch", message)

if __name__ == '__main__':
    unittest.main()
