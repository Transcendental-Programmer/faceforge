#!/usr/bin/env python3
"""
Patch for gradio_client.utils._json_schema_to_python_type function
to handle boolean schema values properly.

This patch adds a check for boolean schema values before trying to access them as dictionaries.
"""

import importlib
import logging

logger = logging.getLogger(__name__)

def apply_patch():
    """Apply the monkey patch to fix the TypeError in gradio_client.utils._json_schema_to_python_type."""
    try:
        # Import the module
        import gradio_client.utils as utils
        
        # Store the original function
        original_func = utils._json_schema_to_python_type
        
        # Define the patched function
        def patched_json_schema_to_python_type(schema, defs=None):
            """Patched version that handles boolean schemas."""
            if schema is None:
                return "None"
            
            # Handle boolean schema values
            if isinstance(schema, bool):
                return str(schema).lower()
                
            # Continue with the original function for non-boolean schemas
            return original_func(schema, defs)
        
        # Apply the patch
        utils._json_schema_to_python_type = patched_json_schema_to_python_type
        
        # Also patch the get_type function
        original_get_type = utils.get_type
        
        def patched_get_type(schema):
            """Patched version of get_type that handles boolean schemas."""
            if isinstance(schema, bool):
                return "bool"
            return original_get_type(schema)
        
        utils.get_type = patched_get_type
        
        logger.info("Successfully applied patch to gradio_client.utils._json_schema_to_python_type")
        return True
    except Exception as e:
        logger.error(f"Failed to apply patch: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Apply the patch
    if apply_patch():
        print("Patch applied successfully.")
    else:
        print("Failed to apply patch.") 