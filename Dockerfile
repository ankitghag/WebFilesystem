FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only required files
COPY main.py .
COPY app/ ./app/

EXPOSE 8000

# Run your entry script (outer main.py)
# CMD ["python", "main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]


#docker build -t webfilesystem-app .

#docker run --env-file .env -p 8000:8000 webfilesystem-app