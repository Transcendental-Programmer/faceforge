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
        
        # Import and run the UI app by default for HF Spaces
        logger.info("Starting in UI mode for Hugging Face Spaces")
        from faceforge_ui.app import create_demo
        demo = create_demo()
        demo.launch(server_name="0.0.0.0", share=False)
            
    except ImportError as e:
        logger.critical(f"Import error: {e}. Please check your dependencies.")
        logger.debug(traceback.format_exc())
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)

# This module is imported by Hugging Face Spaces
if __name__ == "__main__":
    main() 