from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf

# Initialize the FastAPI app
app = FastAPI(title="Fashion MNIST CNN API")

# Load your trained model when the application starts.
# Ensure the 'fashion_mnist_cnn.keras' file is in the same directory.
try:
    model = tf.keras.models.load_model('fashion_mnist_cnn.keras')
except Exception as e:
    raise IOError(f"Error loading model: {e}")

# Define the class names for Fashion-MNIST
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Define the input data model using Pydantic
# The API will expect a JSON object with a key "image"
# containing a 28x28 list of pixel values.
class ImageData(BaseModel):
    image: list

@app.get("/")
def read_root():
    """ A simple endpoint to check if the API is running. """
    return {"message": "Welcome to the Fashion MNIST prediction API!"}

@app.post("/predict/")
def predict_image(data: ImageData):
    """
    Receives image data, preprocesses it, and returns a prediction.
    """
    try:
        # 1. Preprocess the input data
        # Convert the input list to a NumPy array
        image_array = np.array(data.image)

        # The model expects a 4D tensor: (batch_size, height, width, channels)
        # We need to normalize it, reshape it, and add a batch dimension.
        if image_array.shape != (28, 28):
            raise ValueError("Image must be 28x28")

        # Normalize the image data to be between 0 and 1
        image_normalized = image_array / 255.0

        # Add batch and channel dimensions
        image_reshaped = np.expand_dims(image_normalized, axis=0) # (1, 28, 28)
        image_reshaped = np.expand_dims(image_reshaped, axis=-1) # (1, 28, 28, 1)

        # 2. Make a prediction
        prediction = model.predict(image_reshaped)

        # 3. Post-process the prediction
        # Get the index of the highest probability
        predicted_index = np.argmax(prediction[0])
        # Get the corresponding class name
        predicted_class_name = class_names[predicted_index]
        # Get the confidence score
        confidence_score = float(prediction[0][predicted_index])

        # Return the result in a JSON format
        return {
            "predicted_class": predicted_class_name,
            "confidence": f"{confidence_score:.4f}"
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # General exception for other potential errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")