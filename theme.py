import gradio as gr

def get_theme():
    # Digital Noir / Cyberpunk Palette
    c_black = "#020202"  # Deepest black
    c_void = "#080808"   # Slightly lighter black for panels
    c_obsidian = "#0f0f0f" # Element background
    
    c_neon_cyan = "#00f3ff"
    c_neon_magenta = "#ff00ff"
    c_neon_green = "#0aff0a"
    c_alert_red = "#ff2a2a"
    
    c_text_main = "#e0e0e0"
    c_text_dim = "#808080"

    return gr.themes.Default(
        primary_hue=gr.themes.colors.cyan,
        secondary_hue=gr.themes.colors.pink,
        neutral_hue=gr.themes.colors.gray,
        font=[gr.themes.GoogleFont("Share Tech Mono"), "ui-monospace", "monospace"],
    ).set(
        # Body & Backgrounds
        body_background_fill=c_black,
        body_text_color=c_text_main,
        background_fill_primary=c_black,
        background_fill_secondary=c_void,
        
        # Blocks (Panels)
        block_background_fill=c_void,
        block_label_background_fill=c_obsidian,
        block_border_width="1px",
        block_border_color=c_neon_cyan,
        block_title_text_color=c_neon_cyan,
        block_label_text_color=c_neon_cyan,
        block_radius="4px",
        
        # Buttons (Primary - Cyan Neon)
        button_primary_background_fill=c_obsidian,
        button_primary_background_fill_hover="#1a1a1a",
        button_primary_text_color=c_neon_cyan,
        button_primary_border_color=c_neon_cyan,
        button_primary_shadow=f"0 0 10px {c_neon_cyan}",
        
        # Buttons (Secondary - Magenta/Dim)
        button_secondary_background_fill=c_obsidian,
        button_secondary_background_fill_hover="#1a1a1a",
        button_secondary_text_color=c_neon_magenta,
        button_secondary_border_color=c_neon_magenta,
        
        # Inputs & Textboxes
        input_background_fill=c_black,
        input_border_color="#333",
        input_placeholder_color=c_text_dim,
        input_shadow="inset 0 0 5px rgba(0,0,0,0.8)",
        
        # Accents & Borders
        slider_color=c_neon_magenta,
        color_accent=c_neon_cyan,
        border_color_primary=c_neon_cyan,
    )