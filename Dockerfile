FROM python:3.5-alpine

LABEL maintainer="d-Rickyy-b <pastepwn@rickyy.de>"
LABEL site="https://github.com/d-Rickyy-b/pastepwn"

# Create base & log directory
RUN mkdir -p /pastepwn/logs /pastepwn/src
WORKDIR /pastepwn

# Copy the source code to the container
COPY . /pastepwn/src
COPY ./start.sh /pastepwn

# Installation of the pastepwn package
RUN python3 /pastepwn/src/setup.py install
# && pip3 install --no-cache pastepwn

# Start the main file when the container is started
ENTRYPOINT ["/bin/sh", "start.sh"]
