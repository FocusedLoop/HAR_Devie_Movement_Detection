# Raspberry Pi HAR Device Movement Classifier

**Human Activity Recognition (HAR) system running on a Raspberry Pi** that classifies user movement (running, walking, sit-ups, or rest) in real time using trained ML models.

![The HAR device, showcasing the Raspberry Pi setup.](https://raw.githubusercontent.com/username/har-device-classifier/main/images/device_setup.jpg)
![The HAR device in action, detecting and classifying movements.](https://raw.githubusercontent.com/username/har-device-classifier/main/images/device_in_action.jpg)

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Setup & Installation](#setup--installation)
4. [Usage](#usage)
   * [Classification Mode](#classification-mode)
   * [Data-Collection Mode](#data-collection-mode)
5. [Data Collection & Session Instructions](#data-collection--session-instructions)
6. [Troubleshooting & Errors](#troubleshooting--errors)

## Overview
This project implements a **Human Activity Recognition (HAR)** device using a **Raspberry Pi** and an **ADXL343 accelerometer**. We trained **4 different models** on **4,281 rows of movement data** to classify the user's motion as one of:
* **Running**
* **Walking**
* **Sit-ups**
* **Rest**

Using **Scikit-learn**, the following models were developed:
* **MLPClassifier** (Neural Network)
* **Support Vector Classifier (SVC)**
* **KNeighborsClassifier**
* **RandomForestClassifier**

All **trained models** (in `.pkl` format) and a **scaler** file for preprocessing are available in the `models/` folder.

## Features
* **Real-Time Classification**: Continuously detects motion from the ADXL343 sensor.
* **Data Collection**: Easily record new data to enhance or retrain your models.
* **Multiple Models**: Choose from MLP, SVM, KNN, or RF.
* **Sensor Validation**: LED & sensor checks ensure the device is working properly before data collection.

## Setup & Installation

### 1. Hardware Setup
* Connect an **ADXL343 accelerometer** to the Raspberry Pi's **I²C** pins.
* *(Optional)* Connect an **LED** and **button** for device interaction and validation checks.

### 2. Software Setup
* Ensure your Raspberry Pi has **Python 3** and **pip** installed, and that **I²C** is enabled.
* Clone this repository:
```bash
git clone https://github.com/YourUserName/har-device-classifier.git
cd har-device-classifier
```
* Download both required folders:
  * `models/` - Contains all trained classification models and the scaler file
  * `scripts/` - Contains the data collection and classification scripts (final product)

* Run the **setup script** (optional):
```bash
chmod +x device_setup.sh
./device_setup.sh
```
This script installs the necessary Python packages (NumPy, Scikit-learn, Pandas, etc.).

* **Important**: The `models/` folder must be present for the scripts to run properly.

### 3. Choosing a Model
* When prompted, pick one of the **four models**: `mlp`, `svm`, `knn`, or `rf`.
* The **scaler file** (`scaler.pkl`) is used for feature scaling and is located in the `models/` folder.

## Usage

### Classification Mode
Use **har_device_classifier.py** from the `scripts/` folder to classify movements in real time:
```bash
python scripts/har_device_classifier.py
```
* **Model Selection**: Enter `mlp`, `svm`, `knn`, or `rf`.
* The Pi will begin detecting and classifying movements (`running`, `walking`, `sit-ups`, or `rest`).
* Press `CTRL+C` to stop the program.

### Data-Collection Mode
Use **har_device_data_collection.py** from the `scripts/` folder to collect new data:
```bash
python scripts/har_device_data_collection.py
```
* **Session Setup**
   1. Enter your name (session user).
   2. Enter a session ID (an integer).
   3. Specify the movement type (`running`, `walking`, `sit-ups`, `rest`).
* **Validation Checks**
   * Skip? Enter `y` to skip or `n` to run the LED and sensor tests.
   * **LED Test**: LED blinks if working.
   * **Sensor Test**: Prints current time + (x, y, z) readings.
   * If any check fails, the device is not functioning correctly.
* **Recording Data**
   1. Press the **button** to start data collection (LED stays ON).
   2. Move as specified (`running`, `walking`, `sit-ups`, `rest`).
   3. Press the **button** again to end the session.
   4. Press `CTRL+C` to exit at any time.

## Data Collection & Session Instructions
* **Session ID**: Increment this each time you perform an activity.
* **Movement Performed**: Keep a manual note of the movement.
* **Time Per Session**: Aim for ~10 minutes per activity.
* **LED States**:
   * **ON**: Data recording in progress.
   * **OFF**: Device or sensor issue.
   * **BLINKING**: Lost MongoDB connection or database error.

## Troubleshooting & Errors
* **LED OFF during recording** → Check device wiring and sensor logs.
* **BLINKING LED** → Database connection lost; check network or DB status.
* **Repeated Same Label** → Possibly incorrect sensor wiring or wrong model.
* **Program Crash** → Press `CTRL+C` to force stop and check logs for errors.

**Enjoy classifying movements with your Raspberry Pi HAR device!**
