# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install Tesseract-OCR and necessary dependencies
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean

# Copy the application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Flask environment variables
ENV FLASK_APP=app/app.py

# Expose port 5002
EXPOSE 5002

# Run the Flask app using Python
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]
