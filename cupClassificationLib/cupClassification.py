from tensorflow.keras.models import load_model
import cv2
import numpy as np
from cameraLib  import camera

class CupClassification:
    """
    Initializes an instance of CupClassification with a given model.

    Parameters:
    - model_path (str): A string representing the file path to the model.
    - classification_threshold (float): A float representing the classification threshold. Default is 0.5.
    """
    def __init__(self, model_path: str, classification_threshold: float = 0.5) -> None:
        """
        Initialize the CupClassification instance.

        Parameters:
        - model_path (str): A string representing the file path to the model.
        - classification_threshold (float): A float representing the classification threshold. Default is 0.5.
        """
        # Use the path to load the model
        try:
            self.model = load_model(model_path)
            print("Model loaded successfully.")
            
            # Check if the model has the expected input shape
            input_shape = self.model.input_shape[1:]  # Exclude batch size
            expected_shape = (64, 64, 3)
            if input_shape != expected_shape:
                raise ValueError(f"Expected input shape {expected_shape}, but model has input shape {input_shape}")
        except Exception as e:
            print(f"Error loading the model: {e}")
        
        # Set the (default) classification threshold
        self.classification_threshold = classification_threshold

    def classify(self, img: np.ndarray) -> bool:
        """
        Classify the input image and determine if it contains a cup.

        Parameters:
        - img (numpy.ndarray): Input image as a NumPy array with shape (64, 64, 3).

        Returns:
        - bool: True if the model predicts the presence of a cup with confidence above the threshold, False otherwise.

        Raises:
        - ValueError: If the input image shape is not (64, 64, 3).
        """
        if img.shape != (64, 64, 3):
            raise ValueError("Input image shape must be (64, 64, 3)")

        # Transform the data for model input
        X = np.array([img])
        X = X / 255.0

        # Return True if the model predicts the presence of a cup with confidence above the threshold
        predictions = self.model.predict(X)
        return True if predictions[0] > self.classification_threshold else False
    
    def await_classify(self, camera: camera.Camera, timeout: float) -> bool:
        """"""

# test main
if __name__ == '__main__':
    instance = CupClassification('model.h5')
    result = instance.classify(cv2.imread('test-image.jpg', cv2.IMREAD_COLOR))
    print(result)
