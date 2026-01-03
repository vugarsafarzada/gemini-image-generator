#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: The 'google-genai' library is missing. Please run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
if API_KEY == "your_api_key_here":
    raise ValueError("You are using the default placeholder API key. Please update your .env file with a valid Google Cloud API key.")

client = genai.Client(api_key=API_KEY)

def list_available_models():
    """Lists all available models to help debug model name issues."""
    print("Fetching available models...")
    try:
        for model in client.models.list():
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

def enhance_prompt(user_prompt: str) -> str:
    """
    Uses Gemini 2.0 Flash to rewrite the user prompt into a detailed description.
    """
    print(f"Refining prompt: '{user_prompt}'...")
    
    system_instruction = (
        "You are an expert visual prompt engineer. "
        "Rewrite the following short description into a detailed, artistic image generation prompt. "
        "Focus on lighting, texture, style, and composition. Output ONLY the prompt text."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{system_instruction}\n\nInput: {user_prompt}"
        )
        refined_prompt = response.text.strip()
        print(f"Refined Prompt: {refined_prompt}\n")
        return refined_prompt
    except Exception as e:
        print(f"Error during prompt refinement: {e}")
        sys.exit(1)

def generate_image(prompt: str, output_dir: str = "generated_images"):
    """
    Uses Imagen 4 to generate an image from the prompt and saves it.
    """
    print("Generating image with Imagen 4 (this may take a moment)...")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Note: Model name 'imagen-4.0-generate-001' is standard for Imagen 4, 
    # but may vary based on specific API access/beta availability.
    try:
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        for generated_image in response.generated_images:
            image = generated_image.image
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            filename = f"img_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath)
            print(f"Image saved to: {filepath}")
            
            # Open the image automatically
            if sys.platform == "darwin":
                os.system(f"open '{filepath}'")
            elif sys.platform == "win32":
                os.startfile(filepath)
            else:
                os.system(f"xdg-open '{filepath}'")
            
    except Exception as e:
        print(f"Failed to generate image: {e}")

def main():
    parser = argparse.ArgumentParser(description="Gemini CLI Image Generator")
    parser.add_argument("prompt", type=str, nargs="?", help="The text description for the image")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    args = parser.parse_args()

    if args.list_models:
        list_available_models()
        return

    user_prompt = args.prompt

    if not user_prompt:
        prompt_file = Path("prompt.txt")
        if prompt_file.exists():
            print(f"Reading prompt from {prompt_file}...")
            user_prompt = prompt_file.read_text().strip()
        else:
            prompt_file.touch()
            print("There is no prompt or prompt.txt")
            return

    if not user_prompt:
        print("Error: Prompt is empty.")
        return

    refined_prompt = enhance_prompt(user_prompt)
    generate_image(refined_prompt)

if __name__ == "__main__":
    main()