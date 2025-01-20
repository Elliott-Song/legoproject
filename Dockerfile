FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --requirement requirements.txt

# Copy the model
COPY data/models/BestModel.pth data/models/BestModel.pth

# Copy the rest of the code
COPY api.py .

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
# To run this locally do:
# uvicorn api:app --host 0.0.0.0 --port 8080
