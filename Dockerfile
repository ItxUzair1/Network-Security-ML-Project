# Use a lightweight Python image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Install system dependencies required for pip and gunicorn
RUN apk add --no-cache build-base gcc musl-dev libffi-dev

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port (default Flask or Gunicorn port)
EXPOSE 5000

# Command to run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
