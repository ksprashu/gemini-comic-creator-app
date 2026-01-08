import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from PIL import Image

# Add the parent directory to sys.path to find verifier.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verifier import verify_sign_text

@patch('verifier.genai.Client')
def test_verify_sign_text_success(mock_client_cls):
    """Test that verification returns True when Gemini sees the text."""
    # Mock the client
    mock_client = mock_client_cls.return_value
    mock_response = MagicMock()
    mock_response.text = "YES. The image clearly shows a neon sign with the text 'THE TERMINAL'."
    mock_client.models.generate_content.return_value = mock_response

    # Mock an image
    mock_image = Image.new('RGB', (100, 100))

    success, message = verify_sign_text(mock_image)
    
    assert success is True
    assert "Access Granted" in message
    mock_client.models.generate_content.assert_called_once()
    
    # Check prompt contents
    call_args = mock_client.models.generate_content.call_args
    assert "THE TERMINAL" in call_args.kwargs['contents'][0]

@patch('verifier.genai.Client')
def test_verify_sign_text_failure(mock_client_cls):
    """Test that verification returns False when Gemini does not see the text."""
    # Mock the client
    mock_client = mock_client_cls.return_value
    mock_response = MagicMock()
    mock_response.text = "NO. The sign is blurry and unreadable."
    mock_client.models.generate_content.return_value = mock_response

    # Mock an image
    mock_image = Image.new('RGB', (100, 100))

    success, message = verify_sign_text(mock_image)
    
    assert success is False
    assert "verification failed" in message.lower() or "fail" in message.lower()
