import gradio as gr
import requests

def generate_image():
    response = requests.post("http://localhost:8000/generate")
    if response.ok:
        return None  # Placeholder: should return image from backend
    return None

iface = gr.Interface(
    fn=generate_image,
    inputs=[],
    outputs="image",
    title="FaceForge Latent Space Explorer",
    description="Interactively explore and edit faces in latent space."
)

if __name__ == "__main__":
    iface.launch() 