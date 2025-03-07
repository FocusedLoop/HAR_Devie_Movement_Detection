#!/bin/bash

# Setup for running har_device_classsifier.py and har_device_data_collection.py on a Raspberry Pi

# Setup python and I2C dependencies
echo "🔹 Starting installation of dependencies..."
sudo apt update && sudo apt upgrade -y

echo "🔹 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git i2c-tools libatlas-base-dev
echo "🔹 Enabling I2C interface..."
sudo raspi-config nonint do_i2c 0

# Create and activate a virtual environment
echo "🔹 Setting up Python virtual environment..."
python3 -m venv env
source env/bin/activate

pip install --upgrade pip
echo "🔹 Installing Python dependencies..."
pip install numpy==1.26.4 \
            adafruit-circuitpython-busdevice \
            adafruit-circuitpython-adxl34x \
            pymongo \
            gpiozero \
            RPi.GPIO \
            pandas \
            scipy \
            scikit-learn \
            tqdm

echo "nstallation complete! Checking versions..."

# Verify installed versions
python3 -c "
import numpy as np
import pymongo
import adafruit_adxl34x
import gpiozero
import board
import busio
import RPi.GPIO
import pandas as pd
import scipy
import sklearn
import tqdm

print(f'NumPy Version: {np.__version__}')
print(f'PyMongo Version: {pymongo.__version__}')
print(f'Pandas Version: {pd.__version__}')
print(f'Scipy Version: {scipy.__version__}')
print(f'Scikit-Learn Version: {sklearn.__version__}')
print(f'Tqdm Version: {tqdm.__version__}')
print('All dependencies installed successfully!')
"

echo "Setup complete!"
