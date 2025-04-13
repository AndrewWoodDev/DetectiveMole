from keras.classifier_models import load_classifier_model
from PIL import Image, ImageOps
import numpy as np
import streamlit as st

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the classifier_model
classifier_model = load_classifier_model("keras_model.h5", compile=False)

# Load the labels
label_list = open("labels.txt", "r").readlines()

st.title('Is Your Mole Happy?')
st.header('Upload as Image to classify')

img_file = st.file_uploader('Choose the Image...', type=['jpg', 'jpeg', 'png'])

if img_file is not None:
    input_tensor = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your img
    img = Image.open(img_file).convert("RGB")
    st.img(img, caption="Uploaded Image", use_container_width=True)

    # resizing the img to be at least 224x224 and then cropping from the center
    size = (224, 224)
    img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)

    # turn the img into a numpy array
    img_array = np.asarray(img)

    # Normalize the img
    normalized_img_array = (img_array.astype(np.float32) / 127.5) - 1

    # Load the img into the array
    input_tensor[0] = normalized_img_array

    # Predicts the classifier_model
    predictions = classifier_model.predict(input_tensor)
    predicted_index = np.argmax(predictions)
    predicted_label = label_list[predicted_index]
    confidence = predictions[0][predicted_index]

    # Print predictions and confidence score
    st.write(f"Class: {predicted_label[2:].strip()}")
    st.write(f"Confidence Score:{confidence}")
