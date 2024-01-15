# REMOVE IN PRODUCTION VERSION

from cupClassificationLib import cupClassifier
from cameraLib import camera
import time


# Cup threshold and timout values
CUP_TIMEOUT = 999999
CUP_TRESHOLD = 0.75

# Camera sizing, in pixels
CAM_SIZE = 64

cam = camera.Camera(CAM_SIZE)
classifier = cupClassifier.CupClassifier('model.h5', CUP_TRESHOLD)

while True:
        # Capture an image
    img = cam.captureArray()

    # Check for cups
    cupDetected = classifier.classify(img)
    print(cupDetected)
    time.sleep(0.5)



