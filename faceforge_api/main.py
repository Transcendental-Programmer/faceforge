from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FaceForge API is running"}

@app.post("/generate")
def generate_image():
    # Placeholder for image generation logic
    return JSONResponse(content={"status": "success", "image": None}) 