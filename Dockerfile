# Use an official Python runtime as a parent image
FROM arm32v7/python:3.11

# Set the working directory in the container to /app
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip==24.0
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Run main.py when the container launches
CMD ["python", "app.py"]