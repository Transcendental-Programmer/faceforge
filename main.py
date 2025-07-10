#!/usr/bin/env python3
"""
Main entry point for FaceForge application
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

def main():
    """Main function to start the FaceForge application."""
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
        logger.info("Setting up FastAPI application with API and UI")
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
        
        # Create Gradio UI
        logger.info("Creating Gradio UI")
        demo = create_demo()
        
        # Mount Gradio UI
        logger.info("Mounting Gradio UI")
        gr_app = gr.mount_gradio_app(app, demo, path="/")
        
        # Configure server
        import uvicorn
        port = int(os.environ.get("PORT", 7860))
        logger.info(f"Starting integrated server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
            
    except ImportError as e:
        logger.critical(f"Import error: {e}. Please check your dependencies.")
        logger.debug(traceback.format_exc())
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()