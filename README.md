---
title: FaceForge
emoji: 🧑‍🎨
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: "4.44.1"
app_file: app.py
pinned: false
---

# faceforge
Interactive latent space editor for face generation using pretrained GANs and diffusion models.

## 🚀 Deploy on Hugging Face Spaces (Recommended)

FaceForge is ready to run as a Gradio app on [Hugging Face Spaces](https://huggingface.co/spaces):

1. **Push your code to a public GitHub repository.**
2. **Create a new Space** at https://huggingface.co/spaces (choose the Gradio SDK or Docker SDK).
3. **Add your `requirements.txt` and the provided `Dockerfile` to your repo.**
4. **Set the entrypoint to `app.py`** (which integrates both the API and UI components).
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
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
```

## Local Development (Optional)

You can still run FaceForge locally:

```bash
pip install -r requirements.txt
python main.py
```

This will start the integrated application with both the API and UI components available:
- UI accessible at http://localhost:7860/
- API accessible at http://localhost:7860/api/

## Architecture

FaceForge uses a modular architecture:

1. **Core Components** (`faceforge_core/`): Core algorithms and utilities
2. **API Layer** (`faceforge_api/`): FastAPI endpoints for model interaction
3. **UI Layer** (`faceforge_ui/`): Gradio interface for user interaction

The main application integrates these components into a single FastAPI application where:
- The API is mounted at `/api/`
- The Gradio UI is mounted at the root path `/`

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

## Debugging

If you encounter Gradio schema-related errors like:
```
TypeError: argument of type 'bool' is not iterable
```

The application includes a patch that should fix the issue automatically. This patch addresses a known issue with schema processing in older Gradio versions.

### Common Issues:

#### API Connection Errors

If you see errors like:
```
Request failed: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /generate
```

This means the UI can't connect to the API. In the integrated version, the API is available at `/api/generate` rather than a separate server.

To fix this:
1. Ensure you're using the integrated version by running `python main.py`
2. If you need to run the API separately, set the API_URL environment variable:
   ```bash
   API_URL=http://localhost:8000 python faceforge_ui/app.py
   ```

#### Environment Variables

- `MOCK_API`: Set to "true" to use mock API responses (for testing without API)
- `API_URL`: Override the API endpoint URL
- `PORT`: Set the port for the server (default: 7860)

## Notes
- The backend and frontend are fully integrated for Spaces deployment.
- For custom model integration, edit the core and backend modules as needed.
