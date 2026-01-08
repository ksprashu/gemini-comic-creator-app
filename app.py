import os
import re
import gradio as gr
from dotenv import load_dotenv
import google.genai
from theme import get_theme
import logic
import verifier

# Load environment variables
load_dotenv()

# --- Assets ---
ASSETS_DIR = "assets"
IMG_LOCKED = os.path.join(ASSETS_DIR, "ui_locked.png")
IMG_SUCCESS = os.path.join(ASSETS_DIR, "ui_success.png")
IMG_FAIL = os.path.join(ASSETS_DIR, "ui_fail.png")
IMG_BANNER = os.path.join(ASSETS_DIR, "ui_banner_hero.png")

# --- Constants ---
CHAPTERS = ["init", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "epilogue"]

# --- Handlers ---

def run_diagnostics():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        if api_key == "PLACEHOLDER_KEY":
            return "SYSTEM_CHECK: FAILED.\n> API Key: PLACEHOLDER_KEY detected. Please update .env"
        if not re.match(r"^AIza[0-9A-Za-z-_]{35}$", api_key):
             return "SYSTEM_CHECK: WARNING.\n> API Key: Format unrecognized. Proceed with caution.\n> Environment Variables: LOADED"
        return "SYSTEM_CHECK: OPTIMAL.\n> Environment Variables: LOADED\n> API Key: DETECTED (Valid Format)"
    return "SYSTEM_CHECK: FAILED.\n> API Key: MISSING. Please configure .env"

def unlock_chapter(current_chapter, output_log):
    if "OPTIMAL" in output_log or "SUCCESS" in output_log:
        return gr.update(visible=False), gr.update(visible=True)
    return gr.update(visible=True), gr.update(visible=False)

def handle_ch1(prompt):
    img = logic.generate_hero(prompt)
    if not img: return None, "ERROR: No image generated. Check code."
    success, msg = verifier.verify_hero(img)
    log = f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}"
    return img, log

def handle_ch2(sign_text):
    img = logic.generate_sign(sign_text)
    if not img: return None, "ERROR: No image generated."
    success, msg = verifier.verify_sign_text(img, sign_text)
    log = f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}"
    return img, log

def handle_ch3(prompt):
    img = logic.generate_wide_shot(prompt)
    if not img: return None, "ERROR: No image generated."
    success, msg = verifier.verify_aspect_ratio(img)
    log = f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}"
    return img, log

def handle_ch4(prompt):
    img = logic.generate_lit_scene(prompt)
    if not img: return None, "ERROR: No image generated."
    success, msg = verifier.verify_lighting(img)
    log = f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}"
    return img, log

def handle_ch5(prompt, ref_img):
    img = logic.generate_style_transfer(prompt, ref_img)
    if not img: return None, "ERROR: No image generated."
    success, msg = verifier.verify_style(img)
    log = f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}"
    return img, log

def handle_ch6(prompt):
    img = logic.generate_final(prompt)
    if not img: return None, "ERROR: No image generated."
    success, msg = verifier.verify_final(img)
    log = f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}"
    return img, log

# --- UI Builder ---
APP_CSS = """
.gradio-container {font-family: 'Share Tech Mono', monospace;}
.locked-d {filter: grayscale(100%) blur(5px); pointer-events: none;}
"""

with gr.Blocks(title="Gemini Comic Creator") as app:
    
    # State mechanism to track progress 
    # (Simplified: specific outputs trigger specific unlocks)

    with gr.Row():
        gr.Image(IMG_BANNER, show_label=False, container=False)
    
    with gr.Accordion("ACCESS RESTRICTION // CONTENT ADVISORY", open=False):
         gr.Markdown("> **NOTICE:** This simulation contains high-contrast noir themes. User discretion is mandatory.")

    with gr.Tabs() as main_tabs:
        
        # --- INIT ---
        with gr.Tab("INIT // SETUP", id="init") as tab0:
             gr.Markdown("### SYSTEM INITIALIZATION")
             gr.Markdown("Identity verified. Welcome, Artist. Initialize workspace parameters.")
             check_btn = gr.Button("RUN DIAGNOSTICS", variant="primary")
             check_out = gr.Textbox(label="TERMINAL OUTPUT", lines=4)
             
        # --- CH 1 ---
        with gr.Tab("CH 1: INK & FUR", interactive=True, id="ch1") as tab1:
            with gr.Group(visible=True) as lock1:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete INIT diagnostics.")
            
            with gr.Group(visible=False) as content1:
                gr.Markdown("### MISSION: MANIFEST UNIT 9")
                with gr.Row():
                    p1 = gr.Textbox(label="PROMPT", placeholder="Cyberpunk cat...", scale=4)
                    b1 = gr.Button("GENERATE", variant="primary", scale=1)
                with gr.Row():
                    o1 = gr.Image(label="RESULT")
                    l1 = gr.Textbox(label="LOG", lines=3)

        # --- CH 2 ---
        with gr.Tab("CH 2: THE LETTERER", interactive=True, id="ch2") as tab2:
            with gr.Group(visible=True) as lock2:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete CH 1.")
            
            with gr.Group(visible=False) as content2:
                gr.Markdown("### MISSION: THE SILENT SIGN")
                with gr.Row():
                    p2 = gr.Textbox(label="SIGN TEXT", placeholder="THE TERMINAL", scale=4)
                    b2 = gr.Button("GENERATE", variant="primary", scale=1)
                with gr.Row():
                    o2 = gr.Image(label="RESULT")
                    l2 = gr.Textbox(label="LOG", lines=3)

        # --- CH 3 ---
        with gr.Tab("CH 3: WIDE ANGLE", interactive=True, id="ch3") as tab3:
            with gr.Group(visible=True) as lock3:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete CH 2.")
            with gr.Group(visible=False) as content3:
                gr.Markdown("### MISSION: CINEMATIC RATIO")
                with gr.Row():
                    p3 = gr.Textbox(label="PROMPT", placeholder="Chase scene...", scale=4)
                    b3 = gr.Button("GENERATE", variant="primary", scale=1)
                with gr.Row():
                    o3 = gr.Image(label="RESULT")
                    l3 = gr.Textbox(label="LOG", lines=3)

        # --- CH 4 ---
        with gr.Tab("CH 4: MOOD", interactive=True, id="ch4") as tab4:
             with gr.Group(visible=True) as lock4:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete CH 3.")
             with gr.Group(visible=False) as content4:
                gr.Markdown("### MISSION: LIGHTING & ATMOSPHERE")
                with gr.Row():
                    p4 = gr.Textbox(label="PROMPT", placeholder="Neon rain...", scale=4)
                    b4 = gr.Button("GENERATE", variant="primary", scale=1)
                with gr.Row():
                    o4 = gr.Image(label="RESULT")
                    l4 = gr.Textbox(label="LOG", lines=3)

        # --- CH 5 ---
        with gr.Tab("CH 5: STYLE TRAP", interactive=True, id="ch5") as tab5:
             with gr.Group(visible=True) as lock5:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete CH 4.")
             with gr.Group(visible=False) as content5:
                gr.Markdown("### MISSION: STYLE TRANSFER")
                with gr.Row():
                    p5 = gr.Textbox(label="PROMPT", placeholder="Anime style...", scale=3)
                    # We might need a ref image input or assume fixed ref
                    ref5 = gr.Image(label="REFERENCE (Unit 9)", type="pil", scale=1) 
                    b5 = gr.Button("GENERATE", variant="primary", scale=1)
                with gr.Row():
                    o5 = gr.Image(label="RESULT")
                    l5 = gr.Textbox(label="LOG", lines=3)

        # --- CH 6 ---
        with gr.Tab("CH 6: MASTERPIECE", interactive=True, id="ch6") as tab6:
             with gr.Group(visible=True) as lock6:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete CH 5.")
             with gr.Group(visible=False) as content6:
                gr.Markdown("### MISSION: UPSCALING / FINAL")
                with gr.Row():
                    p6 = gr.Textbox(label="PROMPT", placeholder="Masterpiece...", scale=4)
                    b6 = gr.Button("GENERATE", variant="primary", scale=1)
                with gr.Row():
                    o6 = gr.Image(label="RESULT")
                    l6 = gr.Textbox(label="LOG", lines=3)

        # --- EPILOGUE ---
        with gr.Tab("EPILOGUE", interactive=True, id="epilogue") as tabEnd:
             with gr.Group(visible=True) as lockEnd:
                gr.Image(IMG_LOCKED, show_label=False, container=False, width=100)
                gr.Markdown("### 🔒 LOCKED. Complete CH 6.")
             with gr.Group(visible=False) as contentEnd:
                gr.Markdown("# MISSION ACCOMPLISHED")
                gr.Markdown("The comic is complete. The Construct is stable. Well done, Artist.")
                gr.Image(IMG_SUCCESS, show_label=False)

    # --- WIRING ---
    # Init -> Check -> Unlock Ch1
    check_btn.click(run_diagnostics, outputs=check_out).then(unlock_chapter, inputs=[gr.State("init"), check_out], outputs=[lock1, content1])
    
    # Ch1 -> Generate -> Verify -> Unlock Ch2
    b1.click(handle_ch1, inputs=p1, outputs=[o1, l1]).then(unlock_chapter, inputs=[gr.State("ch1"), l1], outputs=[lock2, content2])

    # Ch2 -> Generate -> Verify -> Unlock Ch3
    b2.click(handle_ch2, inputs=p2, outputs=[o2, l2]).then(unlock_chapter, inputs=[gr.State("ch2"), l2], outputs=[lock3, content3])

    # Ch3 -> Generate -> Verify -> Unlock Ch4
    b3.click(handle_ch3, inputs=p3, outputs=[o3, l3]).then(unlock_chapter, inputs=[gr.State("ch3"), l3], outputs=[lock4, content4])

    # Ch4 -> Generate -> Verify -> Unlock Ch5
    b4.click(handle_ch4, inputs=p4, outputs=[o4, l4]).then(unlock_chapter, inputs=[gr.State("ch4"), l4], outputs=[lock5, content5])

    # Ch5 -> Generate -> Verify -> Unlock Ch6
    b5.click(handle_ch5, inputs=[p5, ref5], outputs=[o5, l5]).then(unlock_chapter, inputs=[gr.State("ch5"), l5], outputs=[lock6, content6])

    # Ch6 -> Generate -> Verify -> Unlock Epilogue
    b6.click(handle_ch6, inputs=p6, outputs=[o6, l6]).then(unlock_chapter, inputs=[gr.State("ch6"), l6], outputs=[lockEnd, contentEnd])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)), allowed_paths=["assets"])

