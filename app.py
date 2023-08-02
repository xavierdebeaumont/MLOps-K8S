import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Location Image Classifier")
st.text("Provide URL of Location Image for image classification")

@st.cache_data
def load_model():
  model = tf.keras.models.load_model('/app/models/')
  return model

with st.spinner('Loading Model Into Memory....'):
  model = load_model()

classes = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']

def decode_img(image):
  img = tf.image.decode_jpeg(image, channels=3)  
  img = tf.image.resize(img,[150,150])
  return np.expand_dims(img, axis=0)

path = st.text_input('Enter Image URL to Classify.. ','https://th.bing.com/th/id/R.8014731bbd5a6b57fa772fccb8653038?rik=%2fp%2bNCzs5UuBaug&riu=http%3a%2f%2fwonderfulengineering.com%2fwp-content%2fuploads%2f2014%2f01%2fbuilding-wallpaper.jpeg&ehk=Y6e8DJu5l31WDk1f5XrN%2biuqOrXdC%2fZvh7MMWsbzOc0%3d&risl=&pid=ImgRaw&r=0')
if path is not None:
    content = requests.get(path).content

    st.write("Predicted Class :")
    with st.spinner('classifying.....'):
      label =np.argmax(model.predict(decode_img(content)),axis=1)
      st.write(classes[label[0]])    
    st.write("")
    image = Image.open(BytesIO(content))
    st.image(image, caption='Classifying Image', use_column_width=True)