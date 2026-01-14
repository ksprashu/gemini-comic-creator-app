import os
import io
from google import genai
from google.genai import types
from PIL import Image
from typing import Optional

# Initialize Client
def get_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ GOOGLE_API_KEY not found in environment.")
        return None
    return genai.Client(api_key=api_key)

def _get_image_from_response(response):
    """Helper to extract PIL Image from generate_content response."""
    try:
        # Check for inline_data (standard for images in some SDK versions)
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    return Image.open(io.BytesIO(part.inline_data.data))
                
        # Check if the SDK returns it differently (e.g. specialized response)
        # For gemini-3-pro-image-preview, dynamic typing might return strict objects.
        # But generally, we look for bytes.
        
    except Exception as e:
        print(f"Error parsing response: {e}")
    return None

# --- Chapter 1: Ink & Fur ---
def generate_hero(prompt: str) -> Optional[Image.Image]:
    """
    Chapter 1: Generate Unit 9 (The Cyberpunk Cat).
    Model: gemini-3-pro-image-preview
    """
    client = get_client()
    if not client: return None
    
    print(f"Generating Hero with prompt: {prompt}")
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[prompt]
        )
        return _get_image_from_response(response)
    except Exception as e:
        print(f"Error: {e}")
    
    return None

# --- Chapter 2: The Letterer ---
def generate_sign(sign_text: str) -> Optional[Image.Image]:
    """
    Chapter 2: Generate a neon sign with specific text.
    """
    client = get_client()
    if not client: return None

    base_prompt = "A dark, rainy cyberpunk alleyway with a heavy iron door."
    full_prompt = f"{base_prompt} A neon sign above it reads: '{sign_text}'"
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[full_prompt]
        )
        return _get_image_from_response(response)
    except Exception as e:
        print(f"Error: {e}")
    return None

# --- Chapter 3: The Wide Angle ---
def generate_wide_shot(prompt: str) -> Optional[Image.Image]:
    """
    Chapter 3: Generate a 16:9 wide shot.
    """
    client = get_client()
    if not client: return None
    
    # Codelab Instruction: "Append aspect ratio to the prompt"
    full_prompt = prompt + " Aspect Ratio 16:9"
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[full_prompt]
        )
        return _get_image_from_response(response)
    except Exception as e:
        print(f"Error: {e}")
    return None

# --- Chapter 4: Setting the Mood ---
def generate_lit_scene(prompt: str) -> Optional[Image.Image]:
    """
    Chapter 4: Generate a scene with specific lighting (Chiaroscuro, etc.)
    """
    client = get_client()
    if not client: return None
    
    # User is expected to add lighting keywords to the prompt
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[prompt]
        )
        return _get_image_from_response(response)
    except Exception as e:
        print(f"Error: {e}")
    return None

# --- Chapter 5: The Style Trap ---
def generate_style_transfer(prompt: str, reference_image: Image.Image) -> Optional[Image.Image]:
    """
    Chapter 5: Generate Unit 9 in a specific style using a reference image.
    """
    # TODO: Implement in Chapter 5
    return None

# --- Chapter 6: The Masterpiece ---
def generate_final(prompt: str) -> Optional[Image.Image]:
    """
    Chapter 6: Generate a high-resolution masterpiece.
    """
    # TODO: Implement in Chapter 6
    return None
