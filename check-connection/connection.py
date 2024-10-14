import serial
import time

try:
    # Establish connection to the Arduino on COM10 (adjust port if necessary)
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    # Send data to Arduino
    arduino.write(b'1')  # Send '1' to the Arduino
    print("Sent '1' to Arduino")

    # Wait a moment for the Arduino to respond
    time.sleep(1)

    # Read response from Arduino
    response = arduino.readline().decode('utf-8').strip()  # Read and decode response
    if response:
        print("Arduino response:", response)
    else:
        print("No response from Arduino")

except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")

finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()  # Close the connection
