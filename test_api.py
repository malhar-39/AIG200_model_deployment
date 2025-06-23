import requests
import json
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# --- IMPORTANT: PASTE YOUR LIVE API URL HERE ---
API_URL = "http://fashion-api-app-env.eba-bjtp3vk3.us-east-1.elasticbeanstalk.com/predict/"

# Define the class names to interpret the result
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def display_prediction_window(image_path, prediction_data):
    """Creates a new window to display the image and the prediction result."""
    result_window = tk.Toplevel()
    result_window.title("Prediction Result")
    result_window.geometry("400x450")

    # --- Display Prediction Text ---
    predicted_class = prediction_data.get('predicted_class', 'N/A')
    confidence = prediction_data.get('confidence', 'N/A')
    
    result_label = tk.Label(result_window, text=f"Predicted Class: {predicted_class}", font=("Helvetica", 14))
    result_label.pack(pady=10)
    
    confidence_label = tk.Label(result_window, text=f"Confidence: {confidence}", font=("Helvetica", 12))
    confidence_label.pack(pady=5)

    # --- Display the Original Image ---
    try:
        img = Image.open(image_path)
        img.thumbnail((300, 300))  # Resize for display
        photo = ImageTk.PhotoImage(img)
        
        image_label = tk.Label(result_window, image=photo)
        image_label.image = photo # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)
    except Exception as e:
        print(f"Could not display image: {e}")

    # --- Close Button ---
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack(pady=10)


def predict_user_image():
    """
    Opens a file dialog, sends the selected image to the API,
    and displays the result in a new GUI window.
    """
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select an Image for Prediction",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    try:
        with Image.open(file_path) as img:
            grayscale_img = img.convert('L')
            resized_img = grayscale_img.resize((28, 28))
            image_array = np.array(resized_img)
            image_as_list = image_array.astype(float).tolist()
            json_payload = {"image": image_as_list}

            print(f"Sending image to API...")
            response = requests.post(API_URL, json=json_payload)
            response.raise_for_status()
            prediction_data = response.json()
            print("Response received from API.")

            # Create the results window instead of printing to terminal
            display_prediction_window(file_path, prediction_data)

    except requests.exceptions.HTTPError as err:
        messagebox.showerror("API Error", f"An HTTP error occurred: {err}\nResponse: {err.response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    
    # This keeps the result window open
    root.mainloop()

# Run the function
if __name__ == "__main__":
    predict_user_image()