from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import numpy as np
import os
import tensorflow as tf

tf.compat.v1.disable_eager_execution()

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model_path = os.path.abspath("../models/1")
graph = tf.Graph()
session = tf.compat.v1.Session(graph=graph)
with graph.as_default():
    tf.compat.v1.saved_model.loader.load(
        session,
        [tf.saved_model.SERVING],
        model_path,
    )
    input_tensor = graph.get_tensor_by_name("serving_default_sequential_input:0")
    output_tensor = graph.get_tensor_by_name("StatefulPartitionedCall:0")

class_names = ["Early Blight", "Late Blight", "Healthy"]


def read_file_as_image(data) -> Image.Image:
    image = np.array(Image.open(BytesIO(data)).convert("RGB").resize((256, 256)))
    return image


def predict(image):
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, 0)  # Create a batch

    predictions = session.run(output_tensor, feed_dict={input_tensor: img_array})
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return predicted_class, confidence


@app.get("/alive")
async def alive():
    return {"status": "Alive"}


@app.post("/predict")
async def predict_endpoint(
    file: UploadFile = File(...),
):
    image = read_file_as_image(await file.read())
    predicted_class, confidence = predict(image)
    print(predicted_class, confidence)
    return {"class": predicted_class, "confidence": float(confidence)}
