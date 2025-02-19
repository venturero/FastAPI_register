# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file (created in the next step) into the container
COPY requirements.txt /app/

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . /app/

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
