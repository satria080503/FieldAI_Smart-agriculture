import os
import streamlit as st
import plotly.express as px
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from tensorflow.keras.layers import Layer, LeakyReLU

@tf.keras.utils.register_keras_serializable()
class FixedDropout(Layer):
    def __init__(self, rate, **kwargs):
        seed = kwargs.pop('seed', None)
        noise_shape = kwargs.pop('noise_shape', None)
        super(FixedDropout, self).__init__(**kwargs)
        self.rate = rate

    def call(self, inputs, training=None):
        if not training:
            return inputs
        return tf.nn.dropout(inputs, rate=self.rate)

@tf.keras.utils.register_keras_serializable()
def swish(x):
    return tf.nn.swish(x)

def show_page():
    def get_plant_names():
        supported_plants = ["Apple", "Blueberry", "Cherry", "Corn", "Grape",
                            "Orange", "Peach", "Pepper", "bell", "Potato",
                            "Raspberry", "Soybean", "Squash", "Strawberry", "Tomato"]
        return supported_plants

    def predict(img):
        model = keras.models.load_model("Model/Plant_disease.h5", custom_objects={
            'swish': swish,
            'FixedDropout': FixedDropout,
            'LeakyReLU': LeakyReLU,
        })
        # Load the Image
        img = Image.open(img)

        # Resize Image to size of (224, 224)
        img = img.resize((224, 224))

        # Convert Image to a numpy array
        img = image.img_to_array(img, dtype=np.uint8)

        # Scaling the Image Array values between 0 and 1
        img = np.array(img) / 255.0

        # Ensure the image is in the right format for prediction
        img = np.expand_dims(img, axis=0)

        # Get the Predicted Label for the loaded Image
        prediction = model.predict(img)

        # Label array
        labels = {0: 'Apple___Apple_scab', 1: 'Apple___Black_rot', 2: 'Apple___Cedar_apple_rust', 3: 'Apple___healthy',
                  4: 'Blueberry___healthy', 5: 'Cherry_(including_sour)___healthy', 6: 'Cherry_(including_sour)___Powdery_mildew',
                  7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 8: 'Corn_(maize)___Common_rust_', 9: 'Corn_(maize)___healthy',
                  10: 'Corn_(maize)___Northern_Leaf_Blight', 11: 'Grape___Black_rot', 12: 'Grape___Esca_(Black_Measles)',
                  13: 'Grape___healthy', 14: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 15: 'Orange___Haunglongbing_(Citrus_greening)',
                  16: 'Peach___Bacterial_spot', 17: 'Peach___healthy', 18: 'Pepper,_bell___Bacterial_spot', 19: 'Pepper,_bell___healthy',
                  20: 'Potato___Early_blight', 21: 'Potato___healthy', 22: 'Potato___Late_blight', 23: 'Raspberry___healthy',
                  24: 'Soybean___healthy', 25: 'Squash___Powdery_mildew', 26: 'Strawberry___healthy', 27: 'Strawberry___Leaf_scorch',
                  28: 'Tomato___Bacterial_spot', 29: 'Tomato___Early_blight', 30: 'Tomato___healthy', 31: 'Tomato___Late_blight',
                  32: 'Tomato___Leaf_Mold', 33: 'Tomato___Septoria_leaf_spot', 34: 'Tomato___Spider_mites Two-spotted_spider_mite',
                  35: 'Tomato___Target_Spot', 36: 'Tomato___Tomato_mosaic_virus', 37: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'}

        # Predicted Class
        predicted_class = labels[np.argmax(prediction[0], axis=-1)]

        return [prediction, predicted_class]

    supported_plants = get_plant_names()
    st.write("# Plant Leaf Disease Classification")
    st.write(f"Supported Plants: {', '.join(supported_plants)}")
    st.write("## Upload Image in .jpg format")
    uploaded_image = st.file_uploader("", type=["jpg"])

    st.write("## Uploaded Image")
    if uploaded_image:
        st.image(uploaded_image)

        button = st.button("Classify", key=None)

        if button:
            prediction, predicted_class = predict(uploaded_image)

            labels = {0: 'Apple___Apple_scab', 1: 'Apple___Black_rot', 2: 'Apple___Cedar_apple_rust', 3: 'Apple___healthy',
                      4: 'Blueberry___healthy', 5: 'Cherry_(including_sour)___healthy', 6: 'Cherry_(including_sour)___Powdery_mildew',
                      7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 8: 'Corn_(maize)___Common_rust_', 9: 'Corn_(maize)___healthy',
                      10: 'Corn_(maize)___Northern_Leaf_Blight', 11: 'Grape___Black_rot', 12: 'Grape___Esca_(Black_Measles)',
                      13: 'Grape___healthy', 14: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 15: 'Orange___Haunglongbing_(Citrus_greening)',
                      16: 'Peach___Bacterial_spot', 17: 'Peach___healthy', 18: 'Pepper,_bell___Bacterial_spot', 19: 'Pepper,_bell___healthy',
                      20: 'Potato___Early_blight', 21: 'Potato___healthy', 22: 'Potato___Late_blight', 23: 'Raspberry___healthy',
                      24: 'Soybean___healthy', 25: 'Squash___Powdery_mildew', 26: 'Strawberry___healthy', 27: 'Strawberry___Leaf_scorch',
                      28: 'Tomato___Bacterial_spot', 29: 'Tomato___Early_blight', 30: 'Tomato___healthy', 31: 'Tomato___Late_blight',
                      32: 'Tomato___Leaf_Mold', 33: 'Tomato___Septoria_leaf_spot', 34: 'Tomato___Spider_mites Two-spotted_spider_mite',
                      35: 'Tomato___Target_Spot', 36: 'Tomato___Tomato_mosaic_virus', 37: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'}
            
            print(predict)
            classes = []
            prob = []
            for i, j in enumerate(prediction[0], 0):
                classes.append(labels[i].capitalize())
                prob.append(round(j * 100, 2))

            fig = px.bar(x=classes, y=prob,
                         text=prob, color=classes,
                         labels={"x": "Disease", "y": "Probability(%)"})
            st.markdown("#### Probability Distribution Bar Chart", True)
            st.plotly_chart(fig)

            st.markdown(f"#### The Image Is Classified As `{predicted_class.capitalize()}` With A Probability Of `{max(prob)}%`", True)
    else:
        st.write("#### No Image Was Found, Please Retry!!!")

if __name__ == "__main__":
    show_page()
