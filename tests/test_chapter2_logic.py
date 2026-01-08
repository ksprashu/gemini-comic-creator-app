import pytest
import sys
import os

# Add the parent directory to sys.path to find logic.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import construct_sign_prompt, generate_sign_image
from unittest.mock import MagicMock, patch

def test_construct_sign_prompt_valid():
    """Test that the prompt is correctly constructed with valid input."""
    sign_text = "THE TERMINAL"
    expected_scene = "A dark, rainy cyberpunk alleyway with a heavy iron door and a neon sign above it."
    expected_prompt = f"{expected_scene} A neon sign reads: '{sign_text}'"
    
    result = construct_sign_prompt(sign_text)
    assert result == expected_prompt

def test_construct_sign_prompt_empty():
    """Test that the prompt is constructed even with empty sign text."""
    sign_text = ""
    expected_scene = "A dark, rainy cyberpunk alleyway with a heavy iron door and a neon sign above it."
    expected_prompt = f"{expected_scene} A neon sign reads: ''"
    
    result = construct_sign_prompt(sign_text)
    assert result == expected_prompt

@patch('logic.genai.Client')
def test_generate_sign_image(mock_client_cls):
    """Test generate_sign_image calls the API correctly."""
    # Mock the client instance and its methods
    mock_client = mock_client_cls.return_value
    mock_response = MagicMock()
    # Mock the generated image object
    mock_image = MagicMock() 
    mock_response.generated_images = [MagicMock(image=mock_image)]
    mock_client.models.generate_images.return_value = mock_response

    sign_text = "THE TERMINAL"
    
    # Call the function
    result = generate_sign_image(sign_text)
    
    # Assertions
    assert result == mock_image
    mock_client.models.generate_images.assert_called_once()
    
    # Verify arguments
    call_args = mock_client.models.generate_images.call_args
    assert call_args.kwargs['model'] == 'gemini-3-pro-image-preview'
    # The prompt should contain the sign text and the scene description
    assert "THE TERMINAL" in call_args.kwargs['prompt']
    assert "A dark, rainy cyberpunk alleyway" in call_args.kwargs['prompt']

