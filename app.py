import cv2
import requests
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")

st.title("License Plate Recognition App")

# File upload widget
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg"])

if uploaded_image:
    image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
    success, image_jpg = cv2.imencode('.jpg', image)

    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        headers={'Authorization': f'Token {token}'},
        files={'upload': image_jpg.tobytes()})

    response_json = response.json()
    if response.status_code in [200, 201]:
        response_json = response.json()
        st.write("Recognition Results:")
        st.json(response_json)
    else:
        st.error(f"Request failed with status code: {response.status_code}")

    print(response_json)
