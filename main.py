"""
This file is the main program loop for a larger project that controls the Raspberry Pi's camera and an RFID reader. 
It saves multiple pictures in a folder or path specified by the user of the function and interacts with an RFID reader.

Author: Diego Brandjes
Date:   30-11-2023
"""
from cameraLib import camera
from cupClassificationLib import cupClassifier
from mongoLib  import mongo
from decouple import config
from rfidLib import readerRFID
from i2cLib import bus

import time

SM_PAUSED_STATE  = 2
SM_START = 1
SM_STOP = 0

CUP_TIMEOUT = 10
CUP_TRESHOLD = 0.75

def main():
    uri = config('URI')
    # Initialization of libraries
    i2c = bus.Bus(1, 0x8)
    cam = camera.Camera(64)
    classifier = cupClassifier.CupClassifier('model.h5', CUP_TRESHOLD)
    rfid = readerRFID.Rfid()
    mdb = mongo.Mongo(uri, 'backend', 'cards')

    running = True
    while running:

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

        if cupDetected == True and i2c.send_and_check(SM_START):
            # Code for starting tap here.
            mdb.decreaseBeer()
            
            weightLoop = True
            while weightLoop:
                # This statement will read the weight data only when the read data is within the desired range.
                if i2c.receive_data() > 2 and i2c.receive_data() < 255:
                    weightData = i2c.receive_data()
                    print(weightData) # use for checking
                    weightLoop = False
                    break

        if input("Quit? (y/n): ").strip().lower() == 'y':
            break
        
    rfid.closeGPIO()
    mdb.closeConnection()

if __name__ == "__main__":
    main()
