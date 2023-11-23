from tensorflow.keras.models import load_model
import cv2
import numpy as np

class CupClassification:
    """
    Initializes an instance of CupClassification with a given model.

    Parameters:
    - model (str): A string representing the file path to the model.
    """
    def __init__(self, model_path: str) -> None:
        model = load_model(model_path)
        # Display the loaded model summary
        model.summary()

        X = np.array([cv2.imread('test-image.jpg', cv2.IMREAD_GRAYSCALE)])
        X = X / 255.0

        predictions = model.predict(X)
        print(predictions)

if __name__ == '__main__':
    instance = CupClassification('model.h5')
