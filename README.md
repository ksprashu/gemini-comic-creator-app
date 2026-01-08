# Gemini Comic Creator: Digital Noir

[![Gradio](https://img.shields.io/badge/Gradio-6.x-orange.svg)](https://gradio.app/)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%203-blue.svg)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)

A high-fidelity, progressive storytelling engine built for the **Gemini Comic Creator** codelab. This application leverages Google's state-of-the-art **Gemini 3** models to guide users through a stylized "Digital Noir" comic creation journey.

## 🌃 Overview

Step into the shoes of an Artist in a rainy, cyberpunk future. Your mission is to manifest **Unit 9**, a legendary anthropomorphic cat, through a series of increasingly complex image generation tasks. 

The application utilizes a **Multi-Model Pipeline**:
- **Generation**: `gemini-3-pro-image-preview` for high-fidelity, prompt-driven art.
- **Verification**: `gemini-3-flash-preview` serving as a Visual Language Model (VLM) "Director" that verifies output against chapter requirements.

## 🚀 Features

- **Progressive Unlocking**: A 6-chapter linear narrative. Each chapter's GUI is locked until the previous task's VLM verification passes.
- **VLM Self-Verification**: The system doesn't just generate images; it "sees" them. Gemini 3 Flash acts as an automated judge to ensure users follow thematic and technical guidelines.
- **Digital Noir Aesthetic**: Custom Gradio theme (`Share Tech Mono` font, high-contrast cyan/magenta palette) designed for an immersive cyberpunk experience.
- **Multimodal Tasks**: From basic character inking to complex style transfers using reference images.

## 🛠️ Tech Stack

- **Framework**: [Gradio 6.x](https://gradio.app/)
- **AI SDK**: [`google-genai`](https://pypi.org/project/google-genai/)
- **Environment**: Python 3.13+ managed via [uv](https://github.com/astral-sh/uv)
- **Image Processing**: Pillow

## 📂 Project Structure

```text
app/
├── app.py           # Main Gradio application & UI logic
├── logic.py         # Image generation wrappers (Client implementation)
├── verifier.py      # VLM-based verification logic (The "Director")
├── theme.py         # Custom Cyberpunk/Noir theme definitions
├── assets/          # UI images (banners, locked states, etc.)
├── solutions/       # Completed reference files for codelab steps
└── tests/           # Integrated verification tests
```

## ⚙️ Setup & Installation

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) installed on your system.
- A **Google API Key** with access to Gemini 3 models (Imagen 3 & Gemini 2/3 Flash).

### 2. Environment Configuration
Create a `.env` file in the `app/` directory:
```bash
GOOGLE_API_KEY=your_api_key_here
```

### 3. Install Dependencies
```bash
uv sync
```

### 4. Running the Application
```bash
uv run python app.py
```
The application will be available at `http://localhost:8080`.

## 📖 Codelab Context
This repository is the companion application for the **Gemini Comic Creator** codelab. It is designed to demonstrate "Vibe Coding" where users collaborate with AI to build sophisticated multimodal applications.

---
© 2026 Gemini Labs. Restricted access protocols in effect.
