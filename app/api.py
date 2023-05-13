import os
from flask import Flask, request, Response
from PIL import Image
import numpy as np
import tensorflow as tf
import io
from private_detector.utils.bee_logger import make_logger  # Import bee_logger

app = Flask(__name__)

logger = make_logger("api")  # Create logger instance
logger.debug("Logger initialized")

# Load the pre-trained model
logger.debug(f"Loading model from {os.environ['MODEL_PATH']}")
model = tf.keras.models.load_model(os.environ["MODEL_PATH"])
logger.info("Model loaded successfully")

# Check for the EMOJI environment variable
use_emoji = os.environ.get("EMOJI", "False").lower() == "true"
logger.debug(f"EMOJI setting: {use_emoji}")


def get_emoji(prediction):
    if prediction > 0.7:
        emoji = "🍆"  # Yep, this is a Dingdong
    elif 0.3 < prediction <= 0.7:
        emoji = "🤔"  # Unsure if this is a Trouser snake
    else:
        emoji = "😇"  # Johnson is not here
    return emoji


@app.route("/api/bee_check", methods=["POST"])
def submit_image():
    logger.debug("Received request to /api/bee_check")  # Log new request

    if "image" not in request.files:
        logger.warning("No image provided")  # No image provided
        return {"error": "No image provided"}, 400

    try:
        image_file = request.files["image"]
        image = Image.open(io.BytesIO(image_file.read())).convert("RGB")
        image = image.resize((480, 480))
        image_array = np.array(image) / 255.0
        image_batch = np.expand_dims(image_array, axis=0)
        logger.debug("Image processed successfully")
    except Exception as e:
        # Error processing image
        logger.error(f"Error processing the image: {str(e)}")
        return {"error": "Error processing the image"}, 500

    try:
        prediction = model.predict(image_batch)[0][0]
    except Exception as e:
        logger.error(f"Error during the inference: {str(e)}")  # Log error
        return {"error": "Error during the inference"}, 500

    logger.info(f"Prediction: {float(prediction)}")  # Log prediction

    response = {"prediction": float(prediction)}

    if use_emoji:
        response["tldr"] = get_emoji(prediction)

    return response


@app.route("/health")
def get_health():
    logger.info("Health Check Requested 🐝👩‍⚕️")
    if model is not None:
        # Return an HTTP 200 status to indicate a healthy service
        message = "It's a Match! 🐝🌼 Let's check out some 🍆 🖼️..."
        return Response(message, status=200)
    else:
        # Return an HTTP 503 status to indicate a service unavailable
        message = "The BEEpi is currently unavailable 🐝💔... Please try again later."
        return Response(message, status=503)


if __name__ == "__main__":
    app_port = int(os.environ.get("APP_PORT", 8080))
    logger.debug(f"Starting the application on port {app_port}")
    app.run(host="0.0.0.0", port=app_port)