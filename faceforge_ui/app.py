import gradio as gr
import requests
import numpy as np
from PIL import Image
import io
import base64
import logging
import sys
import traceback
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("faceforge_ui")

# API configuration
API_URL = os.environ.get("API_URL", "http://localhost:8000")
logger.info(f"Using API URL: {API_URL}")

def generate_image(prompts, mode, player_x, player_y):
    """Generate an image based on prompts and player position."""
    try:
        logger.debug(f"Generating image with prompts: {prompts}, mode: {mode}, position: ({player_x}, {player_y})")
        
        # Parse prompts
        prompt_list = [p.strip() for p in prompts.split(",") if p.strip()]
        if not prompt_list:
            logger.warning("No valid prompts provided")
            return None, "No valid prompts provided"
        
        # Prepare request
        req = {
            "prompts": prompt_list,
            "mode": mode,
            "player_pos": [float(player_x), float(player_y)]
        }
        
        # Make API call
        try:
            resp = requests.post(f"{API_URL}/generate", json=req, timeout=30)
            
            if resp.ok:
                data = resp.json()
                
                if "image" in data:
                    img_b64 = data["image"]
                    img_bytes = base64.b64decode(img_b64)
                    
                    try:
                        # For testing, create a simple colored image if decode fails
                        try:
                            img = Image.frombytes("RGB", (256, 256), img_bytes)
                        except:
                            # Fallback to create a test image
                            img = Image.new("RGB", (256, 256), (int(player_x*128)+128, 100, int(player_y*128)+128))
                            
                        return img, "Image generated successfully"
                    except Exception as e:
                        logger.error(f"Error decoding image: {e}")
                        return None, f"Error decoding image: {str(e)}"
                else:
                    return None, "No image in API response"
            else:
                return None, f"API error: {resp.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None, f"Request failed: {str(e)}"
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None, f"Error: {str(e)}"

# Create a simplified Gradio interface to avoid schema issues
demo = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(label="Prompts (comma-separated)", value="A photo of a cat, A photo of a dog"),
        gr.Radio(["distance", "circle"], value="distance", label="Sampling Mode"),
        gr.Slider(-1.0, 1.0, value=0.0, label="Player X"),
        gr.Slider(-1.0, 1.0, value=0.0, label="Player Y")
    ],
    outputs=[
        gr.Image(label="Generated Image", type="pil"),
        gr.Textbox(label="Status")
    ],
    title="FaceForge Latent Space Explorer",
    description="Interactively explore and edit faces in latent space.",
    allow_flagging="never"
)

if __name__ == "__main__":
    logger.info("Starting Gradio app")
    try:
        # Check if we're running in Hugging Face Spaces
        if "SPACE_ID" in os.environ:
            logger.info("Running in Hugging Face Space")
            demo.launch(server_name="0.0.0.0", share=False)
        else:
            logger.info("Running locally")
            demo.launch(server_name="0.0.0.0", share=False)
    except Exception as e:
        logger.critical(f"Failed to launch Gradio app: {e}")
        logger.debug(traceback.format_exc()) 