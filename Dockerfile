# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install cpu requirements
RUN pip install --trusted-host pypi.python.org -r requirements_cpu.txt

# Define environment variable
ENV MODEL_PATH /app/saved_model/

# Download the pretrained model
RUN mkdir -p /app/saved_model && \
    curl -o /app/private_detector.zip https://storage.googleapis.com/private_detector/private_detector.zip && \
    unzip /app/private_detector.zip -d /app/ && \
    rm /app/private_detector.zip

# Set some defaults

ENV EMOJI true
ENV LOG_PRETTY true
# ENV LOG_PATH
ENV LOG_LEVEL INFO
ENV APP_PORT 8080

# Make port available to those outside the bee hive
EXPOSE $APP_PORT

# Run api.py when the container launches
CMD ["python", "api.py"]
