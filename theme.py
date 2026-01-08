import gradio as gr

def get_theme():
    # Define colors
    c_black = "#050505"
    c_dark_gray = "#0a0a0a" 
    c_gray = "#1c1c1c"
    c_cyan = "#00ffff"
    c_magenta = "#ff00ff" 
    c_green = "#00ff00"
    
    return gr.themes.Default(
        primary_hue=gr.themes.colors.cyan,
        secondary_hue=gr.themes.colors.slate,
        neutral_hue=gr.themes.colors.slate,
        font=[gr.themes.GoogleFont("Share Tech Mono"), "ui-monospace", "monospace"],
    ).set(
        # Body
        body_background_fill=c_black,
        body_text_color="#e0e0e0", 
        background_fill_primary=c_black,
        background_fill_secondary=c_dark_gray,
        
        # Block
        block_background_fill=c_dark_gray,
        block_label_background_fill=c_gray,
        block_border_width="1px",
        block_border_color="#333333",
        block_title_text_color=c_cyan,
        block_label_text_color=c_cyan,
        
        # Buttons (Primary - Cyan/Teal)
        button_primary_background_fill="#004d4d", 
        button_primary_background_fill_hover="#008888",
        button_primary_text_color="#ffffff",
        button_primary_border_color=c_cyan,
        
        # Buttons (Secondary - Gray)
        button_secondary_background_fill=c_gray,
        button_secondary_background_fill_hover="#333333",
        button_secondary_text_color="#ffffff",
        button_secondary_border_color="#444",

        # Inputs
        input_background_fill="#080808",
        input_border_color="#444",
        input_placeholder_color="#666",
        
        # Accents
        slider_color=c_magenta,
        color_accent=c_cyan,
    )