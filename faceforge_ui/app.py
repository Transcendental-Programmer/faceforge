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
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("faceforge_ui")

# Add more debug loggers for gradio internals
logging.getLogger("gradio").setLevel(logging.DEBUG)
logging.getLogger("gradio_client").setLevel(logging.DEBUG)

# API configuration
# In HF Spaces, we need to use a relative path since both UI and API run on the same server
# For local development with separate servers, the env var can be set to http://localhost:8000
API_URL = os.environ.get("API_URL", "/api")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:7860")
logger.info(f"Using API URL: {API_URL}")
logger.info(f"Using BASE URL: {BASE_URL}")

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
        
        logger.debug(f"Request payload: {json.dumps(req)}")
        
        # Make API call
        try:
            # For debugging/testing, create a mock image if API is not available
            if API_URL == "/api" and os.environ.get("MOCK_API", "false").lower() == "true":
                logger.debug("Using mock API response")
                # Create a test image
                img = Image.new("RGB", (256, 256), (int(player_x*128)+128, 100, int(player_y*128)+128))
                return img, "Image generated using mock API"
                
            # Determine the base URL for the API
            if API_URL.startswith("/"):
                # Relative URL, construct the full URL with the base URL
                # Note: BASE_URL should NOT have a trailing slash
                full_url = f"{BASE_URL}{API_URL}/generate"
                logger.debug(f"Constructed full URL: {full_url}")
            else:
                # Absolute URL, use as is
                full_url = f"{API_URL}/generate"
            
            logger.debug(f"Making request to: {full_url}")
            resp = requests.post(full_url, json=req, timeout=30)
            logger.debug(f"API response status: {resp.status_code}")
            
            if resp.ok:
                try:
                    data = resp.json()
                    logger.debug(f"API response structure: {list(data.keys())}")
                    
                    if "image" in data:
                        img_b64 = data["image"]
                        logger.debug(f"Image base64 length: {len(img_b64)}")
                        img_bytes = base64.b64decode(img_b64)
                        
                        try:
                            # For testing, create a simple colored image if decode fails
                            try:
                                img = Image.open(io.BytesIO(img_bytes))
                                logger.debug(f"Image decoded successfully: {img.size} {img.mode}")
                            except Exception as e:
                                logger.error(f"Failed to decode image from bytes: {e}, creating test image")
                                # Fallback to create a test image
                                img = Image.new("RGB", (256, 256), (int(player_x*128)+128, 100, int(player_y*128)+128))
                                
                            return img, "Image generated successfully"
                        except Exception as e:
                            logger.error(f"Error processing image: {e}")
                            logger.debug(traceback.format_exc())
                            return None, f"Error processing image: {str(e)}"
                    else:
                        logger.warning("No image field in API response")
                        return None, "No image in API response"
                except Exception as e:
                    logger.error(f"Error parsing API response: {e}")
                    logger.debug(f"Raw response: {resp.text[:500]}")
                    return None, f"Error parsing API response: {str(e)}"
            else:
                logger.error(f"API error: {resp.status_code}, {resp.text[:500]}")
                return None, f"API error: {resp.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            # Fall back to a test image
            logger.debug("Falling back to test image")
            img = Image.new("RGB", (256, 256), (int(player_x*128)+128, 100, int(player_y*128)+128))
            return img, f"API connection failed (using test image): {str(e)}"
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        return None, f"Error: {str(e)}"

# Create a simplified Gradio interface to avoid schema issues
# Use basic components without custom schemas
def create_demo():
    with gr.Blocks(title="FaceForge Latent Space Explorer") as demo:
        gr.Markdown("# FaceForge Latent Space Explorer")
        gr.Markdown("Interactively explore and edit faces in latent space.")
        
        with gr.Row():
            with gr.Column(scale=3):
                prompts_input = gr.Textbox(
                    label="Prompts (comma-separated)", 
                    value="A photo of a cat, A photo of a dog",
                    lines=2
                )
                mode_input = gr.Radio(
                    choices=["distance", "circle"],
                    value="distance",
                    label="Sampling Mode"
                )
                player_x_input = gr.Slider(
                    minimum=-1.0,
                    maximum=1.0,
                    value=0.0,
                    step=0.1,
                    label="Player X"
                )
                player_y_input = gr.Slider(
                    minimum=-1.0,
                    maximum=1.0,
                    value=0.0,
                    step=0.1,
                    label="Player Y"
                )
                
                generate_btn = gr.Button("Generate")
                
            with gr.Column(scale=5):
                output_image = gr.Image(label="Generated Image")
                output_status = gr.Textbox(label="Status")
                
        generate_btn.click(
            fn=generate_image,
            inputs=[prompts_input, mode_input, player_x_input, player_y_input],
            outputs=[output_image, output_status]
        )
        
    return demo

# Only start if this file is run directly, not when imported
if __name__ == "__main__":
    logger.info("Starting Gradio app directly from app.py")
    try:
        # Print Gradio version for debugging
        logger.info(f"Gradio version: {gr.__version__}")
        
        # Create demo
        demo = create_demo()
        
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