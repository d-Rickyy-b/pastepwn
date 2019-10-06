#!/bin/sh
# Starter script for the pastepwn docker image

# If the user provided file does not exist, print an error
if [ ! -f /pastepwn/start.py ]; then
    echo "The file 'start.py' wasn't found!"
    exit 1
else
    python3 /pastepwn/start.py
fi