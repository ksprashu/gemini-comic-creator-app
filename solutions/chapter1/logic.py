import os
from google import genai
from google.genai import types
from PIL import Image

def generate_image(prompt: str) -> Image.Image:
    """
    Generates an image using Gemini 3 Pro Image Preview.
    """
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    try:
        response = client.models.generate_images(
            model='gemini-3-pro-image-preview',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        if response.generated_images:
            return response.generated_images[0].image
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
    return None