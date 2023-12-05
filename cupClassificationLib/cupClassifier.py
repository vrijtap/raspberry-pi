from tensorflow.keras.models import load_model
import cv2
import numpy as np

class CupClassifier:
    """
    Initializes an instance of CupClassification with a given model.

    Parameters:
    - model_path (str): A string representing the file path to the model.
    - classification_threshold (float): A float representing the classification threshold. Default is 0.5.
    """
    def __init__(self, model_path: str, treshold: float) -> None:
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

        # Define the treshold
        self.treshold = treshold

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

        # Convert image to BGR
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Transform the data for model input
        X = np.array([img_bgr])
        X = X / 255.0

        # Return True if the model predicts the presence of a cup with confidence above the threshold
        predictions = self.model.predict(X, verbose=0)
        return True if predictions[0, 0] > self.treshold else False
