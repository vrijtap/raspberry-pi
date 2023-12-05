import smbus2
import time

# i2cBus/bus.py

"""
This module is controlling the I2C connection between the pi and a device on a set port.

Author: Diego Brandjes
Date:   30-11-2023
"""

SM_PAUSED_STATE  = 2
SM_START = 1
SM_STOP = 0

class Bus:

    # start database connection 
    def __init__(self, port, adress):

        # Raspberry Pi I2C Bus
        self.bus = smbus2.SMBus(port)

        # Arduino address
        self.arduino_address = adress
        
    def send_data(self, data):

        try:
            data = int(data)
            self.bus.write_byte(self.arduino_address, data)
        except ValueError as e:
            print(f"Invalid Input: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  # Wait for a while

    def receive_data(self):
        try:

            return self.bus.read_byte(self.arduino_address)
        except Exception as e:
            print("Error setting up the I2C device")

    def send_and_check(self, data):
        try:
            self.send_data(data)
            if self.receive_data() == data:
                print("Message Delivered successfully!")
                return True
            if data == SM_STOP and self.receive_data() == SM_PAUSED_STATE:
                print("Message Delivered successfully!")
                return True
            else:
                print("Error receiving/sending message.")
                return False
        except Exception as e:
            print("Error setting up the I2C device")
            return False