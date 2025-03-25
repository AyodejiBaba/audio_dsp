import os
import pyvisa
import csv
import time
from datetime import datetime

# Set working directory
desired_directory = r"c:\Users\ayode\Downloads\Azure Data Engineer\audio_dsp\lvenergy-results"  # Update your path
os.makedirs(desired_directory, exist_ok=True)  # Ensure directory exists
os.chdir(desired_directory)

print(f"✅ Working directory set to: {os.getcwd()}")

# Initialize VISA connection
rm = pyvisa.ResourceManager()
devices = rm.list_resources()
print("🔍 Available VISA devices:", devices)

try:
    scope = rm.open_resource("USB0::0xF4EC::0xEE38::SDSMMFCD6R2214::INSTR")  # Update your oscilloscope address
    scope.timeout = 10  # Set timeout to 10 seconds
    print(f"✅ Connected to: {scope.query('*IDN?')}")
except Exception as e:
    print(f"❌ Error connecting to oscilloscope: {e}")
    exit()

# Clear scope if necessary
# scope.clear()

# Define measurement queries
measurements = {
    "PKPK": "C1:PAVA? PKPK",
    "RMS": "C1:PAVA? CRMS",
    "FREQ": "C1:PAVA? FREQ"
}

# Create a timestamped CSV filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"measurement_results_{timestamp}.csv"

# Open CSV file and write header
with open(csv_filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "PKPK (V)", "RMS (V)", "Frequency (Hz)"])

    print("📊 Starting measurements...")

    # Collect multiple measurements
    for i in range(3):  # Adjust the number of samples
        timestamp = time.time()  # Get current time
        row_data = [f"{timestamp:.3f}"]  # Format timestamp to 3 decimal places

        for key, command in measurements.items():
            try:
                response = scope.query(command)  # Query oscilloscope
                value = response.split(",")[1].strip()  # Extract value
                numeric_value = float(value.strip("VHz"))  # Convert to float
                formatted_value = f"{numeric_value:.5g}"  # Format to 3 significant figures
                row_data.append(formatted_value)
                print(f"✅ {key}: {formatted_value}")  # Display result
            except Exception as e:
                print(f"⚠️ Error retrieving {key}: {e}")
                row_data.append("ERROR")  # Mark errors in CSV

        # Write row to CSV
        writer.writerow(row_data)
        print(f"💾 Data saved: {row_data}\n")
        time.sleep(1)  # Adjust sampling rate

# Calculate execution time
execution_time = time.time() - timestamp

print(f"✅ Measurement completed. Data saved in: {csv_filename}")
print(f"⏱️ Execution time: {execution_time:.2f} seconds")
