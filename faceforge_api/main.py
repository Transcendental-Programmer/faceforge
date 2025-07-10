from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import numpy as np
import base64
import logging
import sys
import traceback
import io
from PIL import Image
import json

from faceforge_core.latent_explorer import LatentSpaceExplorer
from faceforge_core.attribute_directions import LatentDirectionFinder
from faceforge_core.custom_loss import attribute_preserving_loss

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("faceforge_api")

# --- Models for API ---

class PointIn(BaseModel):
    text: str
    encoding: Optional[List[float]] = Field(None)
    xy_pos: Optional[List[float]] = Field(None)

class GenerateRequest(BaseModel):
    prompts: List[str]
    positions: Optional[List[List[float]]] = Field(None)
    mode: str = "distance"
    player_pos: Optional[List[float]] = Field(None)

class ManipulateRequest(BaseModel):
    encoding: List[float]
    direction: List[float]
    alpha: float

class AttributeDirectionRequest(BaseModel):
    latents: List[List[float]]
    labels: Optional[List[int]] = Field(None)
    n_components: Optional[int] = 10

# --- FastAPI app ---

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global explorer instance
explorer = LatentSpaceExplorer()

# Error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.debug(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(e)},
        )

@app.get("/")
def read_root():
    logger.debug("Root endpoint called")
    return {"message": "FaceForge API is running"}

@app.post("/generate")
async def generate_image(req: GenerateRequest):
    try:
        logger.debug(f"Generate image request: {json.dumps(req.dict(), default=str)}")
        
        # Log request schema for debugging
        logger.debug(f"Request schema: {GenerateRequest.schema_json()}")
        
        # Clear existing points
        explorer.points = []
        
        # Add points for each prompt
        for i, prompt in enumerate(req.prompts):
            logger.debug(f"Processing prompt {i}: {prompt}")
            
            # Generate a mock encoding (in production, this would use a real model)
            encoding = np.random.randn(512)  # Stub: replace with real encoding
            
            # Get position if provided, otherwise None
            xy_pos = req.positions[i] if req.positions and i < len(req.positions) else None
            logger.debug(f"Position for prompt {i}: {xy_pos}")
            
            # Add point to explorer
            explorer.add_point(prompt, encoding, xy_pos)
        
        # Get player position
        if req.player_pos is None:
            player_pos = [0.0, 0.0]
        else:
            player_pos = req.player_pos
        logger.debug(f"Player position: {player_pos}")
        
        # Sample encoding
        logger.debug(f"Sampling with mode: {req.mode}")
        sampled = explorer.sample_encoding(tuple(player_pos), mode=req.mode)
        
        # Generate mock image (in production, this would use the sampled encoding)
        img = (np.random.rand(256, 256, 3) * 255).astype(np.uint8)
        
        # Convert to base64
        logger.debug("Converting image to base64")
        pil_img = Image.fromarray(img)
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        # Prepare response
        response = {"status": "success", "image": img_b64}
        logger.debug(f"Response structure: {list(response.keys())}")
        logger.debug(f"Image base64 length: {len(img_b64)}")
        
        logger.debug("Image generated successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/manipulate")
def manipulate(req: ManipulateRequest):
    try:
        logger.debug(f"Manipulate request: {json.dumps(req.dict(), default=str)}")
        encoding = np.array(req.encoding)
        direction = np.array(req.direction)
        manipulated = encoding + req.alpha * direction
        logger.debug("Manipulation successful")
        return {"manipulated_encoding": manipulated.tolist()}
    except Exception as e:
        logger.error(f"Error in manipulate: {str(e)}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/attribute_direction")
def attribute_direction(req: AttributeDirectionRequest):
    try:
        logger.debug(f"Attribute direction request: {json.dumps(req.dict(), default=str)}")
        latents = np.array(req.latents)
        finder = LatentDirectionFinder(latents)
        
        if req.labels is not None:
            logger.debug("Using classifier-based direction finding")
            direction = finder.classifier_direction(req.labels)
            logger.debug("Direction found successfully")
            return {"direction": direction.tolist()}
        else:
            logger.debug(f"Using PCA with {req.n_components} components")
            components, explained = finder.pca_direction(n_components=req.n_components)
            logger.debug("PCA completed successfully")
            return {"components": components.tolist(), "explained_variance": explained.tolist()}
    except Exception as e:
        logger.error(f"Error in attribute_direction: {str(e)}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e)) 