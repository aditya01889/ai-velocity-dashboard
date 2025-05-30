#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
python3 -m venv /opt/venv
source /opt/venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
