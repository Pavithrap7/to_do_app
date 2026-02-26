# Use official Python base image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Command to run your app
CMD ["python", "app/main.py"]
