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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMG_LOCKED = os.path.join(ASSETS_DIR, "ui_locked.png")
IMG_SUCCESS = os.path.join(ASSETS_DIR, "ui_success.png")
IMG_FAIL = os.path.join(ASSETS_DIR, "ui_fail.png")
IMG_BANNER = os.path.join(ASSETS_DIR, "ui_banner_hero.png")

# --- Constants ---
CHAPTERS = ["init", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "epilogue"]

# --- Handlers ---

def format_log(message, type="info"):
    """Formats a message as HTML with appropriate styling."""
    colors = {
        "info": "#0aff0a",     # Matrix Green
        "success": "#0aff0a",  # Matrix Green
        "warning": "#ffff00",  # Yellow
        "error": "#ff2a2a"     # Alert Red
    }
    color = colors.get(type, "#0aff0a")
    # Convert newlines to breaks for HTML
    html_msg = message.replace("\n", "<br>")
    return f"<div style='color: {color}; font-family: Share Tech Mono, monospace;'>{html_msg}</div>"

def run_diagnostics():
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    # 1. Missing Key
    if not api_key:
        return format_log("SYSTEM_CHECK: FAILED.\n> API Key: MISSING. Please configure .env", "error")
    
    # 2. Placeholder Key
    if api_key == "PLACEHOLDER_KEY":
        return format_log("SYSTEM_CHECK: FAILED.\n> API Key: PLACEHOLDER_KEY detected. Please update .env", "error")
    
    # 3. Invalid Format (Strict Check)
    if not re.match(r"^AIza[0-9A-Za-z-_]{35}$", api_key):
         return format_log("SYSTEM_CHECK: FAILED.\n> API Key: Format unrecognized (Must start with 'AIza').\n> Please verify your GOOGLE_API_KEY in .env", "error")
    
    # 4. Success
    return format_log("SYSTEM_CHECK: OPTIMAL.\n> Environment Variables: LOADED\n> API Key: DETECTED (Valid Format)", "success")

def update_footer(chapter):
    """Updates the footer progress bar based on current chapter."""
    try:
        idx = CHAPTERS.index(chapter)
        progress = (idx / (len(CHAPTERS) - 1)) * 100
    except ValueError:
        progress = 0
    
    # ASCII Progress Bar
    bar_length = 20
    filled_length = int(bar_length * progress // 100)
    bar = "█" * filled_length + "." * (bar_length - filled_length)
    
    return f"SYSTEM STATUS: {int(progress)}% [{bar}] // CURRENT PHASE: {chapter.upper()}"


def unlock_chapter(current_chapter, output_log):
    # Ensure log is a string and handle None
    log_text = str(output_log).upper() if output_log else ""
    
    if "OPTIMAL" in log_text or "SUCCESS" in log_text:
        return gr.update(visible=False), gr.update(visible=True), update_footer(current_chapter)
    return gr.update(visible=True), gr.update(visible=False), gr.update() # No footer update if fail

# Wrapper handlers to catch errors and provide hints
def safe_handle(func, *args):
    try:
        return func(*args)
    except Exception as e:
        msg = f"SYSTEM ERROR: Execution Failed.\n> Traceback: {str(e)}\n\n> HINT: Check your logic.py implementation. Did you return the image object?"
        return None, format_log(msg, "error")

def handle_ch1(prompt):
    return safe_handle(lambda: _handle_ch1_logic(prompt))

def _handle_ch1_logic(prompt):
    img = logic.generate_hero(prompt)
    if not img: return None, format_log("ERROR: No image generated. Check code.", "error")
    success, msg = verifier.verify_hero(img)
    log_type = "success" if success else "error"
    log = format_log(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}", log_type)
    return img, log

def handle_ch2(sign_text):
    return safe_handle(lambda: _handle_ch2_logic(sign_text))

def _handle_ch2_logic(sign_text):
    img = logic.generate_sign(sign_text)
    if not img: return None, format_log("ERROR: No image generated.", "error")
    success, msg = verifier.verify_sign_text(img, sign_text)
    log_type = "success" if success else "error"
    log = format_log(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}", log_type)
    return img, log

def handle_ch3(prompt):
    return safe_handle(lambda: _handle_ch3_logic(prompt))

def _handle_ch3_logic(prompt):
    img = logic.generate_wide_shot(prompt)
    if not img: return None, format_log("ERROR: No image generated.", "error")
    success, msg = verifier.verify_aspect_ratio(img)
    log_type = "success" if success else "error"
    log = format_log(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}", log_type)
    return img, log

def handle_ch4(prompt):
     return safe_handle(lambda: _handle_ch4_logic(prompt))

def _handle_ch4_logic(prompt):
    img = logic.generate_lit_scene(prompt)
    if not img: return None, format_log("ERROR: No image generated.", "error")
    success, msg = verifier.verify_lighting(img)
    log_type = "success" if success else "error"
    log = format_log(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}", log_type)
    return img, log

def handle_ch5(prompt, ref_img):
     return safe_handle(lambda: _handle_ch5_logic(prompt, ref_img))

def _handle_ch5_logic(prompt, ref_img):
    img = logic.generate_style_transfer(prompt, ref_img)
    if not img: return None, format_log("ERROR: No image generated.", "error")
    success, msg = verifier.verify_style(img)
    log_type = "success" if success else "error"
    log = format_log(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}", log_type)
    return img, log

def handle_ch6(prompt):
    return safe_handle(lambda: _handle_ch6_logic(prompt))

def _handle_ch6_logic(prompt):
    img = logic.generate_final(prompt)
    if not img: return None, format_log("ERROR: No image generated.", "error")
    success, msg = verifier.verify_final(img)
    log_type = "success" if success else "error"
    log = format_log(f"VERIFICATION: {'SUCCESS' if success else 'FAILURE'}\n> {msg}", log_type)
    return img, log

# --- UI Builder ---
APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Main Container - Digital Noir Background */
/* Main Container - Digital Noir Background */
.gradio-container {
    background-color: #020202 !important;
    background-image: 
        linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), 
        url('file=assets/ui_background.png');
    background-size: cover;
    background-attachment: fixed;
    color: #e0e0e0 !important;
    min-height: 100vh !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none;
    border-radius: 0;
}

#footer-status {
    flex-shrink: 0;
}

.main-layout {
    flex: 1;
    overflow: hidden;
    min-height: 0;
    gap: 10px;
}

/* Allow panels to scroll internally if needed */
.glass-panel {
    overflow-y: auto;
    max-height: 100%;
    display: flex;
    flex-direction: column;
}

/* Header Image Constraint */
.header-image img {
    max-height: 400px !important; /* Force smaller banner */
    width: auto !important;
    object-fit: contain;
    margin: 0 auto;
}

/* Visualizer Responsive */
.main-visualizer {
    flex: 1;
    height: 100% !important;
    min-height: 0;
    width: 100%;
    object-fit: contain;
    display: flex;
    justify-content: center;
    align-items: center;
}

.main-visualizer img {
    object-fit: contain;
    max-height: 100%;
    width: auto;
}

/* Scanline Effect Overlay (Subtler) */
.scanlines {
    background: linear-gradient(
        to bottom,
        rgba(255,255,255,0),
        rgba(255,255,255,0) 50%,
        rgba(0,0,0,0.1) 50%,
        rgba(0,0,0,0.1)
    );
    background-size: 100% 4px;
    position: fixed;
    pointer-events: none;
    top: 0; right: 0; bottom: 0; left: 0;
    z-index: 999;
    opacity: 0.4;
}

/* Neon Text & Fonts */
.neon-text {
    font-family: 'Share Tech Mono', monospace !important;
    text-shadow: 0 0 2px #00ffff;
}

/* Terminal Log - Styled for HTML output */
.terminal-log-box {
    background-color: #050505 !important;
    color: #0aff0a; /* Default color fallback */
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
    border: 1px solid #333 !important;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    padding: 10px;
    height: 150px; /* Reduced for better fit */
    flex-shrink: 0;
    overflow-y: auto;
}

/* Footer styling - Fixed Bottom Bar look */
#footer-status {
    background-color: #0d0d0d !important;
    border-top: 2px solid #00ffff;
    border-bottom: 1px solid #00ffff;
    color: #00ffff !important;
    font-family: 'Share Tech Mono', monospace !important;
    text-align: center;
    padding: 8px; /* Reduced padding */
    margin-top: 10px;
    font-size: 14px; /* Reduced font size */
    letter-spacing: 2px;
    box-shadow: 0 -5px 15px rgba(0, 255, 255, 0.1);
}

/* Panel Styling */
.glass-panel {
    background: rgba(8, 8, 8, 0.95) !important;
    border: 1px solid rgba(0, 243, 255, 0.2) !important;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    padding: 15px;
    border-radius: 4px;
}

/* Tab Navigation Styling */
.tabs {
    border-bottom: 1px solid #00ffff;
    margin-bottom: 10px;
}

.tab-nav {
    border-bottom: none !important;
    gap: 4px; /* Space between tabs */
}

.tab-nav button {
    border: 1px solid rgba(0, 243, 255, 0.3) !important;
    border-bottom: none !important;
    background: rgba(8, 8, 8, 0.8) !important;
    margin-right: 2px !important;
    border-radius: 4px 4px 0 0 !important;
    color: #808080 !important; /* Default dim */
    transition: all 0.3s ease;
}

.tab-nav button.selected {
    border: 1px solid #00ffff !important;
    border-bottom: 2px solid #000 !important; /* Fake merge with panel */
    background: rgba(0, 243, 255, 0.1) !important;
    color: #00ffff !important;
    text-shadow: 0 0 5px #00ffff;
    font-weight: bold;
}

.access-denied {
    color: #ff2a2a !important; /* Alert Red */
    border: 1px solid #ff2a2a;
    background: rgba(255, 42, 42, 0.1);
    padding: 10px;
    border-radius: 4px;
    font-family: 'Share Tech Mono', monospace;
    animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
    0% { box-shadow: 0 0 5px rgba(255, 42, 42, 0.2); }
    50% { box-shadow: 0 0 15px rgba(255, 42, 42, 0.5); }
    100% { box-shadow: 0 0 5px rgba(255, 42, 42, 0.2); }
}

.mission-header {
    border-left: 3px solid #00ffff;
    padding-left: 10px;
    margin-bottom: 15px;
}

.locked-d {
    filter: grayscale(100%) blur(5px) opacity(0.3);
    pointer-events: none;
}
"""

with gr.Blocks(title="Gemini Comic Creator - Reality Engine", theme=get_theme(), css=APP_CSS) as app:
    
    # State mechanism
    current_chapter_state = gr.State("init")
    
    # Scanline Overlay (Div hack)
    gr.HTML("<div class='scanlines'></div>")

    # --- Header ---
    with gr.Row(elem_classes=["glass-panel", "header-image"]):
        # Removed height constraint for bigger banner
        gr.Image(IMG_BANNER, show_label=False, container=False, interactive=False)
    
    # --- Main Split View ---
    with gr.Row(elem_classes=["main-layout"]):
        
        # === LEFT COLUMN: CONTROL DECK ===
        with gr.Column(scale=1, elem_classes=["glass-panel"]):
            
            with gr.Tabs() as main_tabs:
                
                # --- INIT ---
                with gr.Tab("INIT", id="init") as tab0:
                     gr.Markdown("### > SYSTEM INITIALIZATION")
                     gr.Markdown("*Identity verified. Welcome, Artist.*")
                     gr.Markdown("Initializing connection to Neural Link...")
                     check_btn = gr.Button("RUN DIAGNOSTICS [EXECUTE]", variant="primary")
                
                # --- CH 1 ---
                with gr.Tab("CH 1", id="ch1", interactive=True) as tab1:
                    with gr.Group(visible=True) as lock1:
                        gr.HTML("<div class='access-denied'><h3>🔒 ACCESS DENIED // COMPLETE DIAGNOSTICS</h3></div>")
                    
                    with gr.Group(visible=False) as content1:
                        gr.HTML("<div class='mission-header'><h3>> MISSION: MANIFEST UNIT 9</h3></div>")
                        gr.Markdown("The Construct is empty. Describe the Protagonist to manifest him.")
                        p1 = gr.Textbox(label="INPUT PROMPT", placeholder="Cyberpunk cat detective, neon rain, trenchcoat...", lines=2)
                        b1 = gr.Button("GENERATE [EXECUTE]", variant="primary")

                # --- CH 2 ---
                with gr.Tab("CH 2", id="ch2", interactive=True) as tab2:
                    with gr.Group(visible=True) as lock2:
                        gr.HTML("<div class='access-denied'><h3>🔒 ACCESS DENIED // COMPLETE CH 1</h3></div>")
                    
                    with gr.Group(visible=False) as content2:
                        gr.HTML("<div class='mission-header'><h3>> MISSION: THE SILENT SIGN</h3></div>")
                        gr.Markdown("The sign is blank. Use the prompt to LETTER the sign.")
                        p2 = gr.Textbox(label="SIGN TEXT", placeholder="THE TERMINAL", lines=1)
                        b2 = gr.Button("GENERATE [EXECUTE]", variant="primary")

                # --- CH 3 ---
                with gr.Tab("CH 3", id="ch3", interactive=True) as tab3:
                    with gr.Group(visible=True) as lock3:
                        gr.HTML("<div class='access-denied'><h3>🔒 ACCESS DENIED // COMPLETE CH 2</h3></div>")
                    with gr.Group(visible=False) as content3:
                        gr.HTML("<div class='mission-header'><h3>> MISSION: CINEMATIC RATIO</h3></div>")
                        gr.Markdown("The frame is too tight. Widen the lens to 16:9.")
                        p3 = gr.Textbox(label="INPUT PROMPT", placeholder="High speed chase on cyber-bike...", lines=2)
                        b3 = gr.Button("GENERATE [EXECUTE]", variant="primary")

                # --- CH 4 ---
                with gr.Tab("CH 4", id="ch4", interactive=True) as tab4:
                     with gr.Group(visible=True) as lock4:
                        gr.HTML("<div class='access-denied'><h3>🔒 ACCESS DENIED // COMPLETE CH 3</h3></div>")
                     with gr.Group(visible=False) as content4:
                        gr.HTML("<div class='mission-header'><h3>> MISSION: LIGHTING & ATMOSPHERE</h3></div>")
                        gr.Markdown("It's too dark. Add volumetric lighting and noir atmosphere.")
                        p4 = gr.Textbox(label="INPUT PROMPT", placeholder="Hiding in shadows...", lines=2)
                        b4 = gr.Button("GENERATE [EXECUTE]", variant="primary")

                # --- CH 5 ---
                with gr.Tab("CH 5", id="ch5", interactive=True) as tab5:
                     with gr.Group(visible=True) as lock5:
                        gr.HTML("<div class='access-denied'><h3>🔒 ACCESS DENIED // COMPLETE CH 4</h3></div>")
                     with gr.Group(visible=False) as content5:
                        gr.HTML("<div class='mission-header'><h3>> MISSION: STYLE TRANSFER</h3></div>")
                        gr.Markdown("An imposter appears. Render Unit 9 in a new style (e.g., Anime) using the reference.")
                        p5 = gr.Textbox(label="STYLE PROMPT", placeholder="1980s Anime Style...", lines=2)
                        # We might need a ref image input or assume fixed ref
                        ref5 = gr.Image(label="REFERENCE SOURCE", type="pil", height=150) 
                        b5 = gr.Button("GENERATE [EXECUTE]", variant="primary")

                # --- CH 6 ---
                with gr.Tab("CH 6", id="ch6", interactive=True) as tab6:
                     with gr.Group(visible=True) as lock6:
                        gr.HTML("<div class='access-denied'><h3>🔒 ACCESS DENIED // COMPLETE CH 5</h3></div>")
                     with gr.Group(visible=False) as content6:
                        gr.HTML("<div class='mission-header'><h3>> MISSION: UPSCALING / FINAL</h3></div>")
                        gr.Markdown("Stabilize the Construct. Generate the final 4K masterpiece.")
                        p6 = gr.Textbox(label="INPUT PROMPT", placeholder="Masterpiece, 8k resolution...", lines=2)
                        b6 = gr.Button("GENERATE [EXECUTE]", variant="primary")

                # --- EPILOGUE ---
                with gr.Tab("END", id="epilogue", interactive=True) as tabEnd:
                     with gr.Group(visible=True) as lockEnd:
                        gr.HTML("<div class='access-denied'><h3>🔒 LOCKED</h3></div>")
                     with gr.Group(visible=False) as contentEnd:
                        gr.HTML("<div class='mission-header'><h1>> MISSION ACCOMPLISHED</h1></div>")
                        gr.Markdown("The comic is complete. The Construct is stable. Well done, Artist.")
            
            # --- TERMINAL LOG (Global for Left Column) ---
            gr.Markdown("### > SYSTEM LOG")
            # Changed from Textbox to HTML for strict styling support (Red/Green)
            terminal_log = gr.HTML(label="OUTPUT STREAM", elem_classes=["terminal-log-box"])

        # === RIGHT COLUMN: VISUALIZER ===
        with gr.Column(scale=2, elem_classes=["glass-panel"]):
            gr.Markdown("### > VISUAL FEED")
            # Removed fixed height, added class for CSS control
            visualizer = gr.Image(label="RENDER OUTPUT", interactive=False, elem_id="main-visualizer", elem_classes=["main-visualizer"])


    # --- Footer ---
    footer = gr.Markdown("SYSTEM STATUS: 0% [....................] // CURRENT PHASE: INIT", elem_id="footer-status")

    # --- WIRING ---
    
    # Helper to update footer on unlock
    # We need to chain the output of handle_X -> terminal_log & visualizer
    # Then if success -> unlock next tab -> update footer

    # Init -> Check -> Unlock Ch1
    check_btn.click(run_diagnostics, outputs=terminal_log).then(
        unlock_chapter, 
        inputs=[gr.State("ch1"), terminal_log], 
        outputs=[lock1, content1, footer]
    )
    
    # Ch1 -> Generate -> Verify -> Unlock Ch2
    b1.click(handle_ch1, inputs=p1, outputs=[visualizer, terminal_log]).then(
        unlock_chapter, inputs=[gr.State("ch2"), terminal_log], outputs=[lock2, content2, footer]
    )

    # Ch2 -> Generate -> Verify -> Unlock Ch3
    b2.click(handle_ch2, inputs=p2, outputs=[visualizer, terminal_log]).then(
        unlock_chapter, inputs=[gr.State("ch3"), terminal_log], outputs=[lock3, content3, footer]
    )

    # Ch3 -> Generate -> Verify -> Unlock Ch4
    b3.click(handle_ch3, inputs=p3, outputs=[visualizer, terminal_log]).then(
        unlock_chapter, inputs=[gr.State("ch4"), terminal_log], outputs=[lock4, content4, footer]
    )

    # Ch4 -> Generate -> Verify -> Unlock Ch5
    b4.click(handle_ch4, inputs=p4, outputs=[visualizer, terminal_log]).then(
        unlock_chapter, inputs=[gr.State("ch5"), terminal_log], outputs=[lock5, content5, footer]
    )

    # Ch5 -> Generate -> Verify -> Unlock Ch6
    b5.click(handle_ch5, inputs=[p5, ref5], outputs=[visualizer, terminal_log]).then(
        unlock_chapter, inputs=[gr.State("ch6"), terminal_log], outputs=[lock6, content6, footer]
    )

    # Ch6 -> Generate -> Verify -> Unlock Epilogue
    b6.click(handle_ch6, inputs=p6, outputs=[visualizer, terminal_log]).then(
        unlock_chapter, inputs=[gr.State("epilogue"), terminal_log], outputs=[lockEnd, contentEnd, footer]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0", 
        server_port=8000, 
        allowed_paths=[ASSETS_DIR]
    )
