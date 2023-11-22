import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
# rfidLib/readerRFID.py

"""
This module is controlling the pi's rfid reader/writer.
Please call the closeGPIO function at the end of use to clear the pins.

Author: Diego Brandjes
Date:   05-10-2023
"""
class Rfid:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def write(self, data):
        try:
            print("Now place your tag to write")
            self.reader.write(data)
            

        except Exception as e:
                print(f"An error occured: {e}")

        finally:
            print("Successfully wrote to card!")
            time.sleep(1)


    def read(self):
        while True:
            try:
                print("Reading RFID")
                id, data = self.reader.read()
                time.sleep(0.1)
               
                if len(str(data)) == 48:
                    print("\n__________Card found__________")
                    print(f"UID: {id}\nData: {data}")
                    print("______________________________")

                    data = data[:24]
                    return data
                
            except Exception as e:
                print(f"An error occured: {e}")
    
    def closeGPIO(self):
        GPIO.cleanup()
        print("Cleaned GPIO")
