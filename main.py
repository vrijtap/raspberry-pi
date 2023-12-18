"""
This file is the main program loop for a larger project that controls the Raspberry Pi's camera and an RFID reader. 
It saves an image as an array which is checked for a cup. The program will send out I2C data to a 
slave which responds accordingly. The program will host an API while doing this to hold the value which the slave returns.

Author: Diego Brandjes
Student Number: 500831945
Date:   18-12-2023
"""
from cameraLib import camera
from cupClassificationLib import cupClassifier
from mongoLib  import mongo
from decouple import config
from rfidLib import readerRFID
from i2cLib import bus

from flask import Flask, jsonify
import time
from threading import Thread

app = Flask(__name__)
capacity = 0 # sets global value 'capacity' to zero when starting the program

# State Machine values
SM_PAUSED_STATE  = 2
SM_START = 1
SM_STOP = 0

# Scale max value, used to check for scale data on slave i2c bus.
# Scale modifier, is added on arduino to not conflict with state machine values.
MAX_RETURNED_VALUE = 255
SCALE_MODIFIER = 100

# Cup threshold and timout values
CUP_TIMEOUT = 10
CUP_TRESHOLD = 0.75

# I2C Bus values
I2C_PORT = 1
I2C_ADRESS = 0x08

# Flask API values
API_HOST = '0.0.0.0'
API_PORT = 5000
API_SUCCES = 200

# Camera sizing, in pixels
CAM_SIZE = 64

@app.route('/capacity', methods=['GET'])
def get_integer():
    return jsonify({'capacity of the tank': capacity}), API_SUCCES


# Main program loop
def main():

    global capacity # holds the value of the tank percentage
    uri = config('URI')

    # Initialization of libraries
    i2c = bus.Bus(I2C_PORT, I2C_ADRESS)
    cam = camera.Camera(CAM_SIZE)
    classifier = cupClassifier.CupClassifier('model.h5', CUP_TRESHOLD)
    rfid = readerRFID.Rfid()
    mdb = mongo.Mongo(uri, 'backend', 'cards')

    running = True
    while running:

        # loads the 'capacity' with the filled tank data
        if i2c.receive_data() > SM_PAUSED_STATE and i2c.receive_data() < MAX_RETURNED_VALUE:
            capacity = i2c.receive_data()


        accountLoop = True
        while accountLoop:
            uid = rfid.read() # reads data from card

            if mdb.userExists(uid) == True: 
                accountLoop = False                

        # Loop that checks for the cup being there 
        cupLoop = True
        cupDetected = False
        startTime = time.time()

        while cupLoop:
            # Capture an image
            img = cam.captureArray()

            # Check for cups
            cupDetected = classifier.classify(img)
            
            # Manage the result
            if(cupDetected == True or time.time() - startTime > CUP_TIMEOUT):
                cupLoop = False

        # Sends and checks the starting value for the tap.
        if cupDetected == True and i2c.send_and_check(SM_START):
            
            weightLoop = True
            while weightLoop:

                # Sets state to paused in case the image doesn't contain a cup
                if(classifier.classify(cam.captureArray()) == False and i2c.receive_data() != SM_PAUSED_STATE):
                    i2c.send_and_check(SM_PAUSED_STATE)

                elif(classifier.classify(cam.captureArray() and i2c.receive_data() != SM_START)):
                    i2c.send_and_check(SM_START)

                # This statement will read the weight data only when the read data is within the desired range.
                if (i2c.receive_data() > SM_PAUSED_STATE and i2c.receive_data() < MAX_RETURNED_VALUE and i2c.receive_data() - 10 <= capacity):
                    capacity = i2c.receive_data() - SCALE_MODIFIER # Removes the added modifier to recover the real percentage.
                    print(capacity) # prints capacity for checking only
                    mdb.decreaseBeer()
                    weightLoop = False
                                   
    # Closes the running tasks and joins the threads.
    rfid.closeGPIO()
    mdb.closeConnection()
    flask_thread.join()

# hosts API to hold value returned by the I2C device
def run_flask():
    app.run(host= API_HOST, port= API_PORT)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    main()