# Gemini Image Generator CLI

A powerful command-line interface (CLI) tool that leverages Google's AI models to generate high-quality images. It uses **Gemini 2.0 Flash** to refine and expand your text prompts, and **Imagen 4** to render them into stunning visuals.

## Features

-   **Smart Prompt Refinement:** Automatically enhances short descriptions into detailed, artistic prompts using `gemini-2.0-flash`.
-   **High-Quality Generation:** Generates images using Google's latest `imagen-4.0-generate-001` model.
-   **Flexible Input:** Accepts prompts via command line arguments or a `prompt.txt` file.
-   **Auto-Open:** Automatically opens the generated image in your default viewer (macOS/Windows/Linux).
-   **Secure:** Uses `.env` for API key management.

## Prerequisites

-   Python 3.10 or higher
-   A Google Cloud API Key with access to Gemini and Imagen models.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/gemini-image-generator.git
    cd gemini-image-generator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Create a `.env` file in the root directory and add your key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## Usage

### Basic Usage
Run the script with a text prompt:
```bash
python3 generate.py "A futuristic city on Mars"
```

### Using a Text File
If you run the script without arguments, it looks for a `prompt.txt` file in the current directory:
```bash
python3 generate.py
```

## Output
Generated images are saved in the `generated_images/` folder with a timestamped filename.
