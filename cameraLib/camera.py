from picamera2 import Picamera2
import time
import datetime
import warnings
# cameraLibrary/camera.py

"""
This module is controlling the pi's camera. It will save multiple
pictures in a folder or path specified by the user of the function.

Author: Diego Brandjes
Date:   05-10-2023
"""

# Camera class containing startup of the module and different capture modes. Takes pixel size in int.
class Camera:
    # Picture_size will be used to create an image of corresponding size.
    def __init__(self, picture_size):
        if picture_size < 64:
            picture_size = 64
            warnings.warn("picture_size must be atleast 64. Defaulted to 64...")
        
        self.picture_size = picture_size
        self.picam2 = Picamera2()
        self.__configure_camera()

    # This function sets the size and color of the image.
    def __configure_camera(self):
        camera_config = self.picam2.create_still_configuration(
            main={"size": (self.picture_size, self.picture_size)},
            lores={"size": (self.picture_size, self.picture_size)}
        )
        self.picam2.configure(camera_config)
    #    self.picam2.set_controls({"Saturation": 0.0})  # Sets picture to grayscale

    # Function to take many pictures with a variable amount of time. 
    # Give filepath, name amount of pictures and the time inbetween, in seconds.
    def burst(self, path, name, amount, seconds):
        self.picam2.start()

        for i in range(amount):
            time.sleep(seconds)
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            filename = f"{path}{name}_{i}_{current_datetime}.jpg"
            self.picam2.capture_file(filename)
        self.picam2.stop()

    # Function to make a single picture. Give the filepath and the filename.
    def capture(self, path, name):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.picam2.start()
        filename = f"{path}{name}_{current_datetime}.jpg"
        self.picam2.capture_file(filename)
        self.picam2.stop()

    # Function to capture a picture as an array.
    def captureArray(self):
        self.picam2.start()
        image_array = self.picam2.capture_array()
        self.picam2.stop()
        return image_array
