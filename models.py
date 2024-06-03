from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np


def verifyFingerprint(fingerprint):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("models/fingerprint_Model.h5", compile=False)

    # Load the labels
    class_names = open("models/fingerprint_labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(fingerprint).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = round(prediction[0][index]*100, 2)

    # Print prediction and confidence score
    print("Fingerprint")
    print("Class:", class_name[9:], end="")
    print("Confidence Score:", confidence_score)

    return class_name[9:], confidence_score





def verifyIris(iris):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(iris).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    while(True):
        # Load the model
        left_model = load_model("models/iris_left_Model.h5", compile=False)

        # Load the labels
        left_class_names = open("models/iris_left_labels.txt", "r").readlines()

        # Predicts the model
        prediction = left_model.predict(data)
        left_index = np.argmax(prediction)
        left_class_name = left_class_names[left_index]
        left_confidence_score = round(prediction[0][left_index]*100, 2)

        # Print prediction and confidence score
        print("Left Iris")
        print("Class:", left_class_name[9:], end="")
        print("Confidence Score:", left_confidence_score)

        # Load the model
        right_model = load_model("models/iris_right_Model.h5", compile=False)

        # Load the labels
        right_class_names = open("models/iris_right_labels.txt", "r").readlines()

        # Predicts the model
        prediction = right_model.predict(data)
        right_index = np.argmax(prediction)
        right_class_name = right_class_names[right_index]
        right_confidence_score = round(prediction[0][right_index]*100, 2)

        # Print prediction and confidence score
        print("Right Iris")
        print("Class:", right_class_name[9:], end="")
        print("Confidence Score:", right_confidence_score)

        if left_confidence_score > right_confidence_score and left_confidence_score > 50: # find a better way to do this
            return "Left Iris", left_class_name[9:], left_confidence_score
        elif right_confidence_score > left_confidence_score and right_confidence_score > 50:
            return "Right Iris", right_class_name[9:], right_confidence_score
        else:
            return "", 0, 0 # Figure out a way to send data to indicate no match
