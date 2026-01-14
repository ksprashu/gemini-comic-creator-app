import os
import io
from google import genai
from PIL import Image

def generate_image(prompt: str) -> Image.Image:
    """
    Generates an image using Gemini 3 Pro Image Preview.
    """
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[prompt]
        )
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    return Image.open(io.BytesIO(part.inline_data.data))
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
    return None