#!/usr/bin/env python3
"""
Main entry point for Hugging Face Spaces deployment
"""

import os
import logging
import sys
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("faceforge")

def create_app():
    """Creates and configures the integrated FastAPI application with both API and UI components."""
    try:
        # Apply the patch for Gradio
        logger.info("Applying Gradio patch...")
        try:
            from patch_gradio_utils import apply_patch
            if apply_patch():
                logger.info("Gradio patch applied successfully.")
            else:
                logger.warning("Failed to apply Gradio patch. The app may encounter errors.")
        except Exception as e:
            logger.warning(f"Error applying Gradio patch: {e}")
            logger.debug(traceback.format_exc())
        
        # Set up FastAPI application with both API and UI
        logger.info("Setting up FastAPI application with API and UI for Hugging Face Spaces")
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import gradio as gr
        
        # Import the API and UI components
        from faceforge_api.main import app as api_app
        from faceforge_ui.app import create_demo
        
        # Create a new FastAPI application that will serve as the main app
        app = FastAPI(title="FaceForge")
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount the API under /api
        logger.info("Mounting API at /api")
        app.mount("/api", api_app)
        
        # Set BASE_URL to empty string for HF Spaces deployment
        # This ensures the UI makes relative API requests
        if "BASE_URL" not in os.environ:
            os.environ["BASE_URL"] = ""
            logger.info("Setting BASE_URL to empty string for integrated app")
            
        # Create Gradio UI
        logger.info("Creating Gradio UI")
        demo = create_demo()
        
        # Mount Gradio UI
        logger.info("Mounting Gradio UI")
        gr_app = gr.mount_gradio_app(app, demo, path="/")
        
        return app
    except Exception as e:
        logger.critical(f"Failed to create app: {e}")
        logger.debug(traceback.format_exc())
        raise

# Create the app for Hugging Face Spaces
# This is the entry point that Hugging Face Spaces will use
app = create_app()

if __name__ == "__main__":
    # If this file is run directly, start the server
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    logger.info(f"Starting integrated server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 