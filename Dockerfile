# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install -r requirements.txt

# Make port 5000 and 8000 available to the world outside this container
EXPOSE 5000
EXPOSE 8000

# Run website_monitor.py when the container launches
CMD ["python", "website_monitor.py"]
