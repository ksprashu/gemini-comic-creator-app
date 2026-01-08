import os
import io
import gradio as gr
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
API_KEY = os.environ.get("GOOGLE_API_KEY")
VERIFICATION_MODEL = "gemini-3-flash-preview"

if not API_KEY:
    print("⚠️ Warning: GOOGLE_API_KEY not found.")

# Initialize the Gemini Client
client = genai.Client(api_key=API_KEY)

# --- Helpers ---

def verify_image(image, validation_prompt):
    """
    Verifies image content using Gemini Flash (Fast & Cheap).
    
    Args:
        image: The generated PIL Image.
        validation_prompt: A specific question to ask the model about the image.
                           (e.g. "Is there a cat in this image?")
    
    Returns:
        True if the model answers YES, False otherwise.
    """
    try:
        # We construct a prompt that forces a Boolean-like answer.
        full_prompt = f"Analyze this image. {validation_prompt} Answer ONLY with 'YES' or 'NO'."
        
        response = client.models.generate_content(
            model=VERIFICATION_MODEL,
            contents=[full_prompt, image]
        )
        
        # Simple heuristic: Check if YES is in the response.
        if response.text and "YES" in response.text.upper():
            return True
        return False
        
    except Exception as e:
        print(f"Verification Warning: {e}")
        return True # Fail open on API error to avoid blocking the user flow

def _extract_image(response):
    """Helper to extract PIL Image from Gemini response"""
    if hasattr(response, 'parts'):
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                return Image.open(io.BytesIO(part.inline_data.data))
    
    # Fallback for candidates
    if hasattr(response, 'candidates') and response.candidates:
        if response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return Image.open(io.BytesIO(part.inline_data.data))
    return None

# --- Logic Functions ---

def generate_hero(prompt):
    """Chapter 1: Ink & Fur (Photorealism)"""
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[prompt]
        )
        img = _extract_image(response)
        
        if img:
            # Verification: Ensure the user actually generated a Cyberpunk Cat
            if not verify_image(img, "Is this a Cyberpunk Cat or Feline character?"):
                raise gr.Error("Unit 9 Reject: That doesn't look like me! (Not a Cyberpunk Cat)")
            return img
            
    except Exception as e:
        raise gr.Error(f"Generation Failed: {str(e)}")
    return None

def generate_sign(base_image, sign_text):
    """Chapter 2: The Letterer (Text Rendering)"""
    prompt = f"A neon sign that clearly reads '{sign_text}'."
    try:
        # Multimodal: Pass the base image if available, plus prompt
        contents = [prompt]
        if base_image:
            contents.append(base_image)
            
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=contents
        )
        img = _extract_image(response)
        
        if img:
            # Verification: Check if the text is legible
            if not verify_image(img, f"Is the text '{sign_text}' visible in the image?"):
                gr.Warning("The sign might be hard to read. Try refining the prompt!")
            return img
            
    except Exception as e:
        return None

def generate_wide_shot(prompt):
    """Chapter 3: The Wide Angle (Aspect Ratio)"""
    # Note: Prompting for AR is the most reliable way in v1beta multimodal currently
    full_prompt = prompt + " Aspect Ratio 16:9, cinematic wide shot."
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[full_prompt]
        )
        return _extract_image(response)
    except Exception as e:
        return None

def generate_lit_scene(prompt, lighting_mode):
    """Chapter 4: Setting the Mood (Lighting)"""
    full_prompt = f"{prompt}, {lighting_mode} lighting, cinematic, volumetric fog."
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[full_prompt]
        )
        return _extract_image(response)
    except Exception as e:
        return None

def generate_style_transfer(reference_image, prompt):
    """Chapter 5: The Style Trap (Consistency)"""
    try:
        contents = [prompt]
        if reference_image:
            contents.append(reference_image)
            
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=contents
        )
        img = _extract_image(response)
        
        if img:
            # Verification: Identity Check
            # We want to ensure the STYLE changed, but the SUBJECT matches Unit 9
            if not verify_image(img, "Is this distinctively a Cyberpunk Cat character?"):
                raise gr.Error("Identity Lost: The style transfer erased Unit 9!")
            return img
            
    except Exception as e:
        return None

def generate_final(prompt):
    """Chapter 6: The Masterpiece (Upscaling)"""
    full_prompt = prompt + " highly detailed, 4k resolution, masterpiece, sharp focus."
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[full_prompt]
        )
        return _extract_image(response)
    except Exception as e:
        return None

# --- UI Layout (The "Nano Banana Device" Interface) ---

with gr.Blocks(theme=gr.themes.Glass(), title="Nano Banana Device") as app:
    gr.Markdown("# 🍌 Nano Banana Device: Reality Engine")
    gr.Markdown("### User: The Artist | Target: Unit 9")

    with gr.Tab("1. Manifestation"):
        gr.Markdown("### Chapter 1: Ink & Fur")
        gr.Markdown("*Unit 9 is a wireframe. He needs texture. Describe him.*")
        with gr.Row():
            prompt_1 = gr.Textbox(label="Prompt", placeholder="A cyberpunk cat detective, wet metallic fur...", lines=2)
            btn_1 = gr.Button("MANIFEST", variant="primary")
        out_1 = gr.Image(label="Output")
        btn_1.click(generate_hero, inputs=prompt_1, outputs=out_1)

    with gr.Tab("2. Lettering"):
        gr.Markdown("### Chapter 2: The Letterer")
        gr.Markdown("*The sign is blank. Letter it.*")
        with gr.Row():
            img_2 = gr.Image(label="Template (Optional)", type="pil") 
            text_2 = gr.Textbox(label="Sign Text", value="THE TERMINAL")
            btn_2 = gr.Button("INK SIGN", variant="primary")
        out_2 = gr.Image(label="Output")
        btn_2.click(generate_sign, inputs=[img_2, text_2], outputs=out_2)

    with gr.Tab("3. Layout"):
        gr.Markdown("### Chapter 3: Wide Angle")
        gr.Markdown("*He's crashing into the bezel! Widen the lens to 16:9.*")
        with gr.Row():
            prompt_3 = gr.Textbox(label="Action Prompt", value="Unit 9 riding a light cycle, cinematic")
            btn_3 = gr.Button("WIDEN LENS", variant="primary")
        out_3 = gr.Image(label="Output")
        btn_3.click(generate_wide_shot, inputs=prompt_3, outputs=out_3)

    with gr.Tab("4. Lighting"):
        gr.Markdown("### Chapter 4: Setting the Mood")
        gr.Markdown("*It's too dark. Add volumetric lighting.*")
        with gr.Row():
            prompt_4 = gr.Textbox(label="Scene Description", value="Unit 9 hiding in a warehouse")
            light_4 = gr.Dropdown(["Noir", "Neon", "God Rays"], label="Lighting Style", value="God Rays")
            btn_4 = gr.Button("RELIGHT", variant="primary")
        out_4 = gr.Image(label="Output")
        btn_4.click(generate_lit_scene, inputs=[prompt_4, light_4], outputs=out_4)

    with gr.Tab("5. Style"):
        gr.Markdown("### Chapter 5: The Style Trap")
        gr.Markdown("*Prove identity persists across style changes.*")
        with gr.Row():
            ref_5 = gr.Image(label="Reference Identity", type="pil")
            prompt_5 = gr.Textbox(label="Style Prompt", value="In the style of 1980s Anime")
            btn_5 = gr.Button("TRANSFER", variant="primary")
        out_5 = gr.Image(label="Output")
        btn_5.click(generate_style_transfer, inputs=[ref_5, prompt_5], outputs=out_5)

    with gr.Tab("6. Final"):
        gr.Markdown("### Chapter 6: The Masterpiece")
        gr.Markdown("*Upscale to 4K for the finale.*")
        with gr.Row():
            prompt_6 = gr.Textbox(label="Final Prompt", value="Unit 9 on rooftop at sunrise, masterpiece, 8k")
            btn_6 = gr.Button("RENDER FINAL", variant="primary")
        out_6 = gr.Image(label="Output")
        btn_6.click(generate_final, inputs=prompt_6, outputs=out_6)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))