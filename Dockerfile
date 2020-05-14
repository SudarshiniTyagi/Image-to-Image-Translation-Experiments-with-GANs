# Start with a Linux micro-container to keep the image tiny
FROM ubuntu:latest

# Document who is responsible for this image
MAINTAINER Sudarshini Tyagi "st3688@nyu.edu"

# Install just the Python runtime (no dev)
RUN apt-get update -y && apt-get install -y \
	python-pip \
    python-dev build-essential \
    python3.7 \
    python3-pip \
    libxext6 libxrender-dev libglib2.0-0 libsm6 \
    ca-certificates

# Expose any ports the app is expecting in the environment
ENV PORT 8009
EXPOSE $PORT

# Set up a working folder and install the pre-reqs
WORKDIR /app
ADD requirements.txt /app
RUN pip3 -vvv --no-cache-dir install -r requirements.txt

# Add the code as the last Docker layer because it changes the most
ADD anime-sketch-colorization-with-gans  /app/anime-sketch-colorization-with-gans
ADD GAN-Experiments  /app/GAN-Experiments

# Run the service
CMD [ "python3", "GAN-Experiments/app.py" ]

