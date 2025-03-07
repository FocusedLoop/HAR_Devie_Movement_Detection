import time
import pickle
import warnings
import threading
import adafruit_adxl34x
import board
import busio
import numpy as np

warnings.filterwarnings("ignore")

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_adxl34x.ADXL343(i2c)

# Model Selection
model_type = input("Enter the model type (mlp, svm, knn, or rf):\n")
folder_path = "models/"

with open(folder_path + model_type + '.pkl', 'rb') as file:
    model = pickle.load(file)
with open(folder_path +'scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

data_lock = threading.Lock()
latest_data = {'x': [], 'y': [], 'z': []}

# Collect data from the sensor
def collect_data():
    global latest_data
    while True:
        x_data, y_data, z_data = [], [], []
        for _ in range(30):
            x, y, z = sensor.acceleration
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)
            time.sleep(1/40)

        with data_lock:
            latest_data['x'] = x_data
            latest_data['y'] = y_data
            latest_data['z'] = z_data

# Preprocesse extracted data
class Preprocessing:
    def __init__(self, x_values, y_values, z_values):
        self.x_values = x_values
        self.y_values = y_values
        self.z_values = z_values

    def calculate_mean(self, lst):
        return sum(lst) / len(lst) if lst else 0

    def calculate_range(self, lst):
        return max(lst) - min(lst) if lst else 0

    def calculate_correlation(self, list1, list2):
        return np.corrcoef(list1, list2)[0, 1] if len(list1) > 1 and len(list2) > 1 else 0

    def encode_label(self, lbl):
        label_map = {'situps': 0, 'rest': 1, 'running': 2, 'walking': 3}
        return label_map.get(lbl, -1)

    def calculate_magnitude(self):
        return np.sqrt(np.array(self.x_values)**2 + np.array(self.y_values)**2 + np.array(self.z_values)**2)

    def calculate_mean_acceleration(self):
        magnitudes = self.calculate_magnitude()
        return np.mean(magnitudes)

    def calculate_standard_deviation(self):
        return np.std([np.mean(self.x_values), np.mean(self.y_values), np.mean(self.z_values)])

    def calculate_rms(self):
        magnitudes = self.calculate_magnitude()
        return np.sqrt(np.mean(magnitudes**2))

    def calculate_peak_to_peak(self):
        return np.ptp([max(self.x_values), max(self.y_values), max(self.z_values),
                       min(self.x_values), min(self.y_values), min(self.z_values)])

    def calculate_sma(self):
        return np.mean(np.abs(self.x_values) + np.abs(self.y_values) + np.abs(self.z_values))

    def calculate_zero_crossing_rate(self, values):
        signal = np.array(values)
        return np.sum((signal[:-1] * signal[1:]) < 0)

    def calculate_autocorrelation(self, values):
        n = len(values)
        if n < 2:
            return 0
        mean = np.mean(values)
        autocorr = np.correlate(values - mean, values - mean, mode='full')[-n:]
        return autocorr.mean() / (np.var(values) * np.arange(n, 0, -1)).mean()

    def extract_features(self):
        features = {
            # Mean values
            'x_means': self.calculate_mean(self.x_values),
            'y_means': self.calculate_mean(self.y_values),
            'z_means': self.calculate_mean(self.z_values),

            # Ranges
            'x_range': self.calculate_range(self.x_values),
            'y_range': self.calculate_range(self.y_values),
            'z_range': self.calculate_range(self.z_values),

            # Correlations
            'xy_corr': self.calculate_correlation(self.x_values, self.y_values),
            'yz_corr': self.calculate_correlation(self.y_values, self.z_values),
            'xz_corr': self.calculate_correlation(self.x_values, self.z_values),

            # Acceleration metrics
            'mean_acceleration': self.calculate_mean_acceleration(),
            'std_acceleration': self.calculate_standard_deviation(),
            'rms_acceleration': self.calculate_rms(),
            'peak_to_peak_amplitude': self.calculate_peak_to_peak(),

            # Magnitude-based features
            'magnitude_acceleration': self.calculate_mean_acceleration(),
            'signal_magnitude_area': self.calculate_sma(),

            # Zero-crossing rates
            'zero_crossing_rate_x': self.calculate_zero_crossing_rate(self.x_values),
            'zero_crossing_rate_y': self.calculate_zero_crossing_rate(self.y_values),
            'zero_crossing_rate_z': self.calculate_zero_crossing_rate(self.z_values),

            # Autocorrelation
            'autocorrelation_x': self.calculate_autocorrelation(self.x_values),
            'autocorrelation_y': self.calculate_autocorrelation(self.y_values),
            'autocorrelation_z': self.calculate_autocorrelation(self.z_values),
        }
        return features

# Updates the values lastes_data in the heap while collecting new values
def update_prediction():
    global latest_data
    label_map = {0: 'situps', 1: 'rest', 2: 'running', 3: 'walking'}

    while True:
        time.sleep(0.1) 

        with data_lock:
            x_list, y_list, z_list = latest_data['x'], latest_data['y'], latest_data['z']

        if not x_list or not y_list or not z_list:  
            continue

        def extract_and_predict():
            preprocessor = Preprocessing(x_list, y_list, z_list)
            features = preprocessor.extract_features()

            feature_values = list(features.values())
            scaled_features = scaler.transform([feature_values])
            predicted_label = model.predict(scaled_features)[0]
            movement_prediction = label_map.get(predicted_label, "Unknown")

            print(f"Predicted movement: {movement_prediction}")

        feature_thread = threading.Thread(target=extract_and_predict)
        feature_thread.start()

# Collect data then classify movement
data_thread = threading.Thread(target=collect_data, daemon=True)
data_thread.start()

prediction_thread = threading.Thread(target=update_prediction, daemon=True)
prediction_thread.start()

while True:
    time.sleep(1)