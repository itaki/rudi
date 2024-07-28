import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# ADS1115 board address and pin setup for TableSaw
BOARD_ADDRESS = 0x49  # 74 in decimal
PIN_NUMBER = ADS.P0

# Constants for standard deviation calculation
SAMPLE_SIZE = 100
STD_DEV_MULTIPLIER = 2  # Multiplier for on/off determination

def calculate_std_dev(values):
    mean = np.mean(values)
    variance = np.mean([(x - mean) ** 2 for x in values])
    return np.sqrt(variance)

def main():
    try:
        ads = ADS.ADS1115(i2c, address=BOARD_ADDRESS)
        chan = AnalogIn(ads, PIN_NUMBER)
        print(f"⚡⚡⚡⚡⚡⚡⚡⚡ Adding Voltage Sensor on pin {PIN_NUMBER} on ADS1115 at address {hex(BOARD_ADDRESS)}")
    except Exception as e:
        print(f"■■■■■ ERROR! ■■■■■■  ADS1115 not found at {hex(BOARD_ADDRESS)}. Cannot create voltage sensor: {e}")
        return

    readings = []
    
    # Initial sampling to determine baseline and standard deviation
    for _ in range(SAMPLE_SIZE):
        reading = chan.voltage
        readings.append(reading)
    
    mean_reading = np.mean(readings)
    std_dev = calculate_std_dev(readings)
    threshold = std_dev * STD_DEV_MULTIPLIER
    print(f"Initialized Mean: {mean_reading:.4f}, Standard Deviation: {std_dev:.4f}, Threshold: {threshold:.4f}")

    while True:
        reading = chan.voltage
        readings.append(reading)
        if len(readings) > SAMPLE_SIZE:
            readings.pop(0)
        
        current_mean = np.mean(readings)
        current_std_dev = calculate_std_dev(readings)
        
        print(f"Current Voltage: {reading:.4f} V, Mean: {current_mean:.4f} V, Std Dev: {current_std_dev:.4f} V")

        if abs(reading - mean_reading) > threshold:
            print("TableSaw is ON")
        else:
            print("TableSaw is OFF")

if __name__ == "__main__":
    main()
