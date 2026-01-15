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
            contents=["Answer strictly YES or NO. " + prompt, image]
        )
        text = response.text.strip().upper()
        return "YES" in text, text
    except Exception as e:
        return False, f"System Error: {e}"

# --- Chapter 1: Hero Verification ---
def verify_hero(image: Image.Image) -> tuple[bool, str]:
    """Verifies if the image matches 'Unit 9' (Cyberpunk Cat)."""
    if image is None: return False, "No image generated."
    
    # Stricter check: Must be a CAT, Cyberpunk, and NOIR. explicitly check for "Pink Panther" style mismatch if needed,
    # but primarily verify it looks "Gritter" and not just a generic cartoon.
    prompt = (
        "Is this image explicitly showcasing a 'Cyberpunk Cat Detective'? "
        "It MUST have ALL of the following: "
        "1. A Cat (humanoid/anthropomorphic) with fur. "
        "2. Cyberpunk elements (neon, tech, trenchcoat). "
        "3. A gritty, dark, cool, or 'Noir' atmosphere. "
        "4. It MUST NOT look like the 'Pink Panther' cartoon character (pink skin/fur without grit). "
        "Is this a valid Unit 9?"
    )
    success, text = verify_image_content(image, prompt)
    if success:
        return True, "Identity Confirmed: Unit 9 is online."
    return False, "Subject Mismatch. We need a GRITTY CYBERPUNK CAT. Ensure keywords like 'Cyberpunk', 'Trenchcoat', 'Neon', 'Rain' are present. Avoid generic cartoons."

# --- Chapter 2: Sign Verification ---
def verify_sign_text(image: Image.Image, expected_text: str = "THE TERMINAL") -> tuple[bool, str]:
    """Verifies if the neon sign is legible."""
    if image is None: return False, "No image generated."
    
    prompt = (
        f"Look at the text in the image. Does it CLEARLY read '{expected_text}'? "
        "The text must be purely '{expected_text}' (case insensitive) and highly legible on a NEON SIGN or similar display. "
        "If the text is gibberish, misspelled, or missing, answer NO."
    )
    success, text = verify_image_content(image, prompt)
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
    
    prompt = (
        "Does this image showcase dramatic, cinematic lighting? "
        "It MUST have clear evidence of 'Chiaroscuro', 'Volumetric Lighting', 'God Rays', or strong contrast between light and shadow. "
        "It should NOT be flatly lit. Is the lighting dramatic and atmospheric?"
    )
    success, text = verify_image_content(image, prompt)
    if success:
        return True, "Atmosphere Stabilized. Lighting is cinematic."
    return False, "Scene is flat. Add terms like 'Volumetric Lighting', 'Chiaroscuro', or 'Neon Glow'."

# --- Chapter 5: Style Verification ---
def verify_style(image: Image.Image) -> tuple[bool, str]:
    """Verifies style transfer (e.g., Anime)."""
    if image is None: return False, "No image generated."
    
    prompt = (
        "Is this image rendered in a distinct 2D Animation style (like 1980s Anime, Cel-Shaded, or Manga)? "
        "It should NOT look photorealistic. It should look hand-drawn or cel-shaded. "
        "Is the style clearly 'Anime' or 'Vintage Animation'?"
    )
    success, text = verify_image_content(image, prompt)
    if success:
        return True, "Style Transfer Complete. Metric: 1980s Anime."
    return False, "Style Mismatch. Ensure you are requesting '1980s Anime Style' or 'Cel Shaded'."

# --- Chapter 6: Final Verification ---
def verify_final(image: Image.Image) -> tuple[bool, str]:
    """Verifies quality/masterpiece status."""
    if image is None: return False, "No image generated."
    
    prompt = (
        "Is this image of exceptionally high quality, looking like a finished 'Masterpiece' or 'High Resolution' art piece? "
        "It should be sharp, detailed, and free of obvious 'rough draft' artifacts. "
        "Does it look like a final, polished 8K render?"
    )
    success, text = verify_image_content(image, prompt)
    if success:
        return True, "Resolution: 8K. Detail: Maximum. Masterpiece Created."
    return False, "Quality Low. Enhance! Use keywords: 'Masterpiece', 'High Resolution', '8k', 'Highly Detailed'."
