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
    """
    Generate an image based on prompts and player position.
    
    Args:
        prompts: Comma-separated list of prompts
        mode: Sampling mode ('distance' or 'circle')
        player_x: X-coordinate of player position
        player_y: Y-coordinate of player position
    
    Returns:
        PIL.Image or None: Generated image or None if generation failed
    """
    try:
        logger.debug(f"Generating image with prompts: {prompts}, mode: {mode}, position: ({player_x}, {player_y})")
        
        # Parse prompts
        prompt_list = [p.strip() for p in prompts.split(",") if p.strip()]
        if not prompt_list:
            logger.warning("No valid prompts provided")
            return None
        
        logger.debug(f"Parsed prompts: {prompt_list}")
        
        # Prepare request
        req = {
            "prompts": prompt_list,
            "mode": mode,
            "player_pos": [float(player_x), float(player_y)]
        }
        
        logger.debug(f"Sending request to API: {req}")
        
        # Make API call
        try:
            resp = requests.post(f"{API_URL}/generate", json=req, timeout=30)
            logger.debug(f"API response status: {resp.status_code}")
            
            if resp.ok:
                data = resp.json()
                logger.debug("Successfully received API response")
                
                if "image" in data:
                    img_b64 = data["image"]
                    img_bytes = base64.b64decode(img_b64)
                    
                    try:
                        img = Image.frombytes("RGB", (256, 256), img_bytes)
                        logger.debug("Successfully decoded image")
                        return img
                    except Exception as e:
                        logger.error(f"Error decoding image: {e}")
                        logger.debug(traceback.format_exc())
                        return None
                else:
                    logger.warning("No image in API response")
                    return None
            else:
                logger.error(f"API error: {resp.status_code} - {resp.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            logger.debug(traceback.format_exc())
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        return None

# Create Gradio interface
logger.info("Initializing Gradio interface")
with gr.Blocks() as demo:
    gr.Markdown("# FaceForge Latent Space Explorer")
    
    with gr.Row():
        with gr.Column():
            prompts = gr.Textbox(
                label="Prompts (comma-separated)", 
                value="A photo of a cat, A photo of a dog",
                info="Enter prompts separated by commas"
            )
            mode = gr.Radio(
                choices=["distance", "circle"], 
                value="distance", 
                label="Sampling Mode",
                info="Choose how to sample the latent space"
            )
            player_x = gr.Slider(-1.0, 1.0, value=0.0, label="Player X")
            player_y = gr.Slider(-1.0, 1.0, value=0.0, label="Player Y")
            btn = gr.Button("Generate")
        
        with gr.Column():
            img = gr.Image(label="Generated Image")
            status = gr.Textbox(label="Status", interactive=False)
    
    def on_generate_click(prompts, mode, player_x, player_y):
        try:
            logger.info("Generate button clicked")
            result = generate_image(prompts, mode, player_x, player_y)
            if result is not None:
                return [result, "Image generated successfully"]
            else:
                return [None, "Failed to generate image. Check logs for details."]
        except Exception as e:
            logger.error(f"Error in generate button handler: {e}")
            logger.debug(traceback.format_exc())
            return [None, f"Error: {str(e)}"]
    
    btn.click(
        fn=on_generate_click,
        inputs=[prompts, mode, player_x, player_y],
        outputs=[img, status]
    )
    
    demo.load(lambda: "Ready to generate images", outputs=status)

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