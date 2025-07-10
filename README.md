# faceforge
Interactive latent space editor for face generation using pretrained GANs and diffusion models.

## 🚀 Deploy on Hugging Face Spaces (Recommended)

FaceForge is ready to run as a Gradio app on [Hugging Face Spaces](https://huggingface.co/spaces):

1. **Push your code to a public GitHub repository.**
2. **Create a new Space** at https://huggingface.co/spaces (choose the Gradio SDK or Docker SDK).
3. **Add your `requirements.txt` and the provided `Dockerfile` to your repo.**
4. **Set the entrypoint to `faceforge_ui/app.py`** (the Gradio app).
5. **Deploy!** Your app will be live at `https://<your-username>.hf.space`.

### Example Dockerfile (already included):
```Dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "faceforge_ui/app.py"]
```

## Local Development (Optional)

You can still run FaceForge locally:

```bash
pip install -r requirements.txt
python faceforge_ui/app.py
```

## Features
- Latent space exploration and manipulation
- Attribute direction discovery (PCA/classifier)
- Custom attribute-preserving loss
- Modular, testable core
- Gradio UI for interactive exploration

## Controls (Gradio UI)
- Enter prompts (comma-separated)
- Choose sampling mode (distance/circle)
- Adjust player position sliders
- Click "Generate" to see results

## Testing
Run all tests with:
```bash
pytest tests/
```

## Notes
- The backend and frontend are fully integrated for Spaces.
- For custom model integration, edit the core and backend modules as needed.
