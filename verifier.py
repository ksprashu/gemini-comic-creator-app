import os
from google import genai
from google.genai import types
from PIL import Image

def get_client():
    return genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def verify_image_content(image: Image.Image, prompt: str) -> tuple[bool, str]:
    """Helper to verify image content using Gemini 3 Flash."""
    client = get_client()
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=["Answer YES or NO. " + prompt, image]
        )
        text = response.text.strip().upper()
        return "YES" in text, text
    except Exception as e:
        return False, f"System Error: {e}"

# --- Chapter 1: Hero Verification ---
def verify_hero(image: Image.Image) -> tuple[bool, str]:
    """Verifies if the image matches 'Unit 9' (Cyberpunk Cat)."""
    if image is None: return False, "No image generated."
    
    success, text = verify_image_content(image, "Is this a humanoid or anthropomorphic cyberpunk cat? It should look cool and noir.")
    if success:
        return True, "Identity Confirmed: Unit 9 is online."
    return False, "Subject Mismatch. We need a Cyberpunk Cat. Try keywords: 'Anthropomorphic Cat', 'Cyberpunk', 'Noir'."

# --- Chapter 2: Sign Verification ---
def verify_sign_text(image: Image.Image, expected_text: str = "THE TERMINAL") -> tuple[bool, str]:
    """Verifies if the neon sign is legible."""
    if image is None: return False, "No image generated."
    
    success, text = verify_image_content(image, f"Does this image clearly show a neon sign with the text '{expected_text}'? The text must be legible.")
    if success:
        return True, f"Text Verified: '{expected_text}' is lit."
    return False, f"Text Illegible. Ensure the prompt asks for a 'Neon Sign' that 'Reads {expected_text}'."

# --- Chapter 3: Aspect Ratio Verification ---
def verify_aspect_ratio(image: Image.Image, target_ratio: str = "16:9") -> tuple[bool, str]:
    """Verifies image dimensions."""
    if image is None: return False, "No image generated."
    
    w, h = image.size
    ratio = w / h
    
    # 16:9 is ~1.77. Allow tolerance.
    target = 16/9
    if abs(ratio - target) < 0.2:
        return True, "Wide Angle Lens Confirmed (16:9)."
    
    return False, f"Aspect Ratio Mismatch. Current: {ratio:.2f}. Target: 1.77 (16:9). Did you append 'Aspect Ratio 16:9'?"

# --- Chapter 4: Lighting Verification ---
def verify_lighting(image: Image.Image) -> tuple[bool, str]:
    """Verifies cinematic lighting."""
    if image is None: return False, "No image generated."
    
    success, text = verify_image_content(image, "Does this image have dramatic lighting? Look for 'Chiaroscuro', 'Rim Light', 'God Rays', or 'Neon' glow. Is it atmospheric?")
    if success:
        return True, "Atmosphere Stabilized. Lighting is cinematic."
    return False, "Scene is flat. Add terms like 'Volumetric Lighting', 'Chiaroscuro', or 'Neon Glow'."

# --- Chapter 5: Style Verification ---
def verify_style(image: Image.Image) -> tuple[bool, str]:
    """Verifies style transfer (e.g., Anime)."""
    if image is None: return False, "No image generated."
    
    success, text = verify_image_content(image, "Is this image in the style of 1980s Anime or Vintage Animation? It should look hand-drawn or cel-shaded.")
    if success:
        return True, "Style Transfer Complete. Metric: 1980s Anime."
    return False, "Style Mismatch. Ensure you are using the Reference Image and requesting '1980s Anime Style'."

# --- Chapter 6: Final Verification ---
def verify_final(image: Image.Image) -> tuple[bool, str]:
    """Verifies quality/masterpiece status."""
    if image is None: return False, "No image generated."
    
    success, text = verify_image_content(image, "Is this image high quality, detailed, and looking like a finished masterpiece? It shouldn't look blurry or draft-like.")
    if success:
        return True, "Resolution: 8K. Detail: Maximum. Masterpiece Created."
    return False, "Quality Low. Enhance! Use keywords: 'Masterpiece', 'High Resolution', '8k', 'Highly Detailed'."
