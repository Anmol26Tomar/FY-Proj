# Scholar-Agent Backend

This backend exposes the Scholar-Agent multi-agent workflow via a FastAPI server.

## Local Development
1. Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python main.py
   ```
   Or explicitly via uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API runs locally on `http://localhost:8000`. You can visit `http://localhost:8000/docs` to see the interactive Swagger UI.

## Deployment Guide (Production)

To deploy this backend API, you can use rendered services like **Render**, **Railway**, **Heroku**, or deploy directly on a VPS (like **AWS EC2**, **DigitalOcean Droplet**) using Docker.

### Option A: Deploying via Render/Railway
These platforms build directly from your GitHub repository.
1. Push this code to a GitHub repo.
2. In the platform dashboard, create a "New Web Service".
3. Point it to your GitHub repository.
4. Set the Start Command to:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Set environment variables if needed (e.g., `OLLAMA_API_URL` or `GROQ_API_KEY` for real implementation).

### Option B: Dockerized Deployment
For VPS, it is best to use Docker.
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
2. Build and Run:
   ```bash
   docker build -t scholar-agent-backend .
   docker run -d -p 8000:8000 scholar-agent-backend
   ```
