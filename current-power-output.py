import os
import pyvisa
import csv
import time
from datetime import datetime

# Set working directory
desired_directory = r"c:\Users\ayode\Downloads\Azure Data Engineer\audio_dsp\lvenergy-results"  # Update path
os.makedirs(desired_directory, exist_ok=True)
os.chdir(desired_directory)

print(f"✅ Working directory set to: {os.getcwd()}")

# Initialize VISA connection
rm = pyvisa.ResourceManager()
devices = rm.list_resources()
print("🔍 Available VISA devices:", devices)

try:
    scope = rm.open_resource("USB0::0xF4EC::0xEE38::SDSMMFCD6R2214::INSTR")  # Update oscilloscope address
    scope.timeout = 10  # Set timeout to 10 seconds
    print(f"✅ Connected to: {scope.query('*IDN?')}")
except Exception as e:
    print(f"❌ Error connecting to oscilloscope: {e}")
    exit()

# Define measurement queries
measurements = {
    "Voltage RMS": "C1:PAVA? CRMS",  # RMS voltage across shunt resistor
    "Voltage PK-PK": "C1:PAVA? PKPK",  # Peak-to-peak voltage
    "Frequency": "C1:PAVA? FREQ"
}

# Create a timestamped CSV filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"measurement_results_{timestamp}.csv"

# Open CSV file and write header
with open(csv_filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Voltage RMS (V)", "Voltage PK-PK (V)", "Frequency (Hz)", "Current RMS (A)", "Current PK-PK (A)", "Power RMS (W)", "Power PK-PK (W)"])

    print("📊 Starting measurements...")

    # Collect multiple measurements
    for i in range(3):  # Adjust the number of samples
        timestamp = time.time()
        row_data = [f"{timestamp:.3f}"]
        voltage_rms, voltage_pkpk, frequency = None, None, None

        for key, command in measurements.items():
            try:
                response = scope.query(command)
                value = response.split(",")[1].strip()
                numeric_value = float(value.strip("VHz"))
                formatted_value = f"{numeric_value:.5g}"
                row_data.append(formatted_value)
                print(f"✅ {key}: {formatted_value}")
                
                # Store values for calculations
                if key == "Voltage RMS":
                    voltage_rms = numeric_value
                elif key == "Voltage PK-PK":
                    voltage_pkpk = numeric_value
                elif key == "Frequency":
                    frequency = numeric_value
            except Exception as e:
                print(f"⚠️ Error retrieving {key}: {e}")
                row_data.append("ERROR")

        # Calculate current and power using R = 100Ω
        if voltage_rms is not None and voltage_pkpk is not None:
            current_rms = voltage_rms / 100  # Ohm's Law: I = V/R
            current_pkpk = voltage_pkpk / 100  # Ohm's Law: I = V/R
            power_rms = voltage_rms * current_rms  # P = V * I
            power_pkpk = voltage_pkpk * current_pkpk  # P = V * I
            row_data.extend([f"{current_rms:.5g}", f"{current_pkpk:.5g}", f"{power_rms:.5g}", f"{power_pkpk:.5g}"])
            print(f"✅ Current RMS: {current_rms:.5g} A, Current PK-PK: {current_pkpk:.5g} A, Power RMS: {power_rms:.5g} W, Power PK-PK: {power_pkpk:.5g} W")
        else:
            row_data.extend(["ERROR", "ERROR", "ERROR", "ERROR"])

        writer.writerow(row_data)
        print(f"💾 Data saved: {row_data}\n")
        time.sleep(1)  # Adjust sampling rate

print(f"✅ Measurement completed. Data saved in: {csv_filename}")