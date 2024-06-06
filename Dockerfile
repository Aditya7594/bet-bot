# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the bot files into the container
COPY . .

# Install any dependencies needed for the bot
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the bot runs on
EXPOSE 8080

# Command to run the bot when the container starts
CMD ["python", "main.py"]
