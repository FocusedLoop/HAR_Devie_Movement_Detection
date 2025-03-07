import time
from datetime import datetime
import board
import busio
import adafruit_adxl34x
from pymongo import MongoClient, errors
from gpiozero import LED, Button
import logging
import threading

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO Pin and Mongo URL setup
LED_PIN = 17
BUTTON_PIN = 18  
MONGO_URI = ""

# Initialize GPIO, I2C and sensor
led = LED(LED_PIN)
button = Button(BUTTON_PIN)
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_adxl34x.ADXL343(i2c)

# Grab accelerometer data from the sensor
def collect_data():
    measurements = {"x_values": [], "y_values": [], "z_values": []}
    start_time = datetime.now()
    
    try:
        for i in range(60):  # Collect 60 samples
            x, y, z = sensor.acceleration
            measurements["x_values"].append(x)
            measurements["y_values"].append(y)
            measurements["z_values"].append(z)
            time.sleep(1/20)  # Collect at 20Hz
        logging.info("Data collection completed.")
    except Exception as e:
        logging.error(f"Error collecting data from sensor: {e}")
        return None, None
    
    return measurements, start_time

# Validate accelerometer data
def validate_data(data):
    if not data.get('x_values') or not data.get('y_values') or not data.get('z_values'):
        logging.error("Error: Missing data fields!")
        return False
    return True

# Upload accelerometer data
def upload_data(measurements, start_time):
    global state
    if validate_data(measurements) == False:
        return
    
    if measurements is None:
        logging.warning("No data to upload due to previous errors.")
        return

    document = {
        "timestamp": start_time,
        "x_values": measurements["x_values"],
        "y_values": measurements["y_values"],
        "z_values": measurements["z_values"],
        "Movement_label": movementID,
        "Session_ID": user + "_" + sessionID,
    }
    
    try:
        data_collection.insert_one(document)
        logging.info("Data uploaded to MongoDB successfully.")
    except Exception as e:
        logging.error(f"Error uploading data to MongoDB: {e}")
        flash_led(5)
        state = "INACTIVE"
        logging.info("Transitioned to INACTIVE state.")


# Flash LED
def flash_led(amount):
    for i in range(amount):
        time.sleep(0.5)
        led.on()
        time.sleep(0.5)
        led.off()

# Setup session
user = input("Who is starting the current session?\n")
sessionID = input("What is the current session number (running, walking, situps or rest)?\n")
movementID = input("What is the movement type being performed?\n")

# Component Validation
logging.info("Commencing Component Validation\n")

if input("Skip validation(Y or N)").upper() == "N":
    logging.info("LED TESTING")
    flash_led(3)

    logging.info("SENSOR TESTING")
    time.sleep(0.5)
    for i in range(3):
        measurements, timestamp = collect_data()
        print(f"timestamp: {timestamp}",
              f"\nx_values: {measurements['x_values']}",
              f"\ny_values: {measurements['y_values']}",
              f"\nz_values: {measurements['z_values']}",
              )
        time.sleep(0.5)

    logging.info("VALIDATION COMPLETE")

# Start MongoDB connection
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["IAB330_Group13"]
    data_collection = db["movement_data"]
    logging.info("Connected to MongoDB successfully.")
except errors.ConnectionFailure as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    exit(1)
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    exit(1)

logging.info("HAR DEVICE IS READY FOR USE")

# MongoDB Transmission state
state = "INACTIVE"

# Detect button press
def handle_button_press():
    global state
    if state == "INACTIVE":
        time.sleep(0.01)
        state = "ACTIVE"
        led.on()
        logging.info("Transitioned to ACTIVE state.")
    else:
        state = "INACTIVE"
        led.off()
        logging.info("Transitioned to INACTIVE state.")

# Monitor accelerometer
last_reading = None
consecutive_unresponsive = 0
consecutive_readings = 0
unresponsive_threshold = 10
reading_threshold = 10

def monitor_system():
    global last_reading, consecutive_unresponsive, consecutive_readings, state
    
    while True:
        try:
            # Check for mongoDB connection
            client.admin.command('ping')

            # Check for accelerometer data
            current_reading = sensor.acceleration
            
            if current_reading == last_reading:
                consecutive_unresponsive += 1
                consecutive_readings += 1
            else:
                consecutive_unresponsive = 0
                consecutive_readings = 0
            
            # Check for unresponsive accelerometer
            if consecutive_unresponsive >= unresponsive_threshold:
                logging.error("Error: Accelerometer is unresponsive")
                led.off()
                continue

            # Check for repeated accelerometer data
            if consecutive_readings >= reading_threshold:
                logging.error(f"Repeated data values detected at {time.time()}")
                led.off()
                break

            last_reading = current_reading
        except Exception as e:
            logging.error(f"Error reading accelerometer: {e}")
            state = "INACTIVE"
            led.off()
            logging.info("Transitioned to INACTIVE state.")
        time.sleep(1)

button.when_pressed = handle_button_press

# Main loop: on button press, light LED and send accelerometer data to MongoDB
try:
    monitor_thread = threading.Thread(target=monitor_system, daemon=True)
    monitor_thread.start()
    while True:
        if state == "ACTIVE":
            start_time = time.time()
            measurements, window_start_time = collect_data()
            
            # Ensure 3 seconds has passed
            while time.time() - start_time < 3.0:
                time.sleep(0.1)
            
            upload_data(measurements, window_start_time)
        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    logging.info("Program terminated by user.")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
finally:
    led.off()
    logging.info("Program exited gracefully.")