
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files into the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the Flask application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
