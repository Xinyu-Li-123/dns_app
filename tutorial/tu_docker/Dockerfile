# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# ENV PORT=8080

# Expose the port the app runs on
EXPOSE 8080

# Print some text to the console
RUN echo "Hello World from Docker container at $(pwd)"

RUN ls -lh 

RUN python --version

RUN pip list

# Run the command to start the app
CMD ["python3", "myapp.py"]