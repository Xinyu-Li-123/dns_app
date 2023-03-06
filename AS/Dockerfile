# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /AS

# Copy the requirements file into the container at /AS 
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /AS 
COPY . .

ENV PORT=53533

# Expose the port the app runs on
EXPOSE 53533

# Print some text to the console
RUN echo "Hello World from Docker image for Authoritative server at $(pwd)"

# RUN ls -lh 

# RUN python --version

# RUN pip list

# Run the command to start the app
CMD ["python3", "as_app.py"]
