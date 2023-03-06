# run a simple python UDP socket server

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /FS
WORKDIR /server

# Copy the current directory contents into the container at /FS
COPY . .

ENV PORT=5005

# Expose the port the app runs on
EXPOSE 5005

# Print some text to the console
RUN echo "Hello World from Docker image for UDP-socket Server at $(pwd)"

# Run the command to and start the app
CMD ["python3", "server.py"]