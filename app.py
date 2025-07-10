import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("faceforge_app")

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    logger.info("Starting FaceForge app")
    # Import the demo from the UI module
    from faceforge_ui.app import demo
    
    # Launch the app
    if __name__ == "__main__":
        logger.info("Launching Gradio interface")
        demo.launch(server_name="0.0.0.0")
except Exception as e:
    logger.critical(f"Failed to start app: {e}")
    import traceback
    logger.debug(traceback.format_exc())
    raise 