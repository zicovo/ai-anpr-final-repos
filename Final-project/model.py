# Imports for driver detector
import numpy as np
import cv2
import math
import tensorflow as tf


# Imports for phone use detector
from tensorflow import keras
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import os


# Load driver detector model
tf.keras.backend.clear_session()
driver_detector_path = "./models/driver"
driver_model = tf.saved_model.load(driver_detector_path)


# Driver detector functions
def load_image_driver(path):
    image = cv2.imread(path)
    resized_img = cv2.resize(image, (512, 512))
    np_image = np.array(resized_img).astype(np.uint8)
    return np_image


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            output_dict['detection_masks'], output_dict['detection_boxes'],
            image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                           tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

    return output_dict


def detect_driver(path):
    # Load Image
    image_np = load_image_driver(path)
    # Predict
    output_dict = run_inference_for_single_image(driver_model, image_np)

    # get position of max certain driver pos
    driver_pos_percentage = output_dict['detection_boxes'][0]
    y, x = image_np.shape[:-1]
    driver_pos = [math.floor(driver_pos_percentage[0] * y), math.floor(driver_pos_percentage[2] * y),
                  math.floor(driver_pos_percentage[1] * x), math.floor(driver_pos_percentage[3] * x)]

    # add to y & x to make image 112x112
    y_extra = (112 - (driver_pos[1] - driver_pos[0])) / 2
    x_extra = (112 - (driver_pos[3] - driver_pos[2])) / 2
    driver_pos_224 = [driver_pos[0] - math.floor(y_extra), driver_pos[1] + math.ceil(y_extra),
                      driver_pos[2] - math.floor(x_extra), driver_pos[3] + math.ceil(x_extra)]

    # crop & reshape image to 224 x 224
    cropped_image_224 = image_np[driver_pos_224[0]:driver_pos_224[1], driver_pos_224[2]:driver_pos_224[3]]

    # basename
    basename = os.path.basename(path)
    try:
        resized_img_224 = cv2.resize(cropped_image_224, (224, 224))
        cv2.imwrite(f'./cropped/driver/{basename}', resized_img_224)
    except Exception as e:
        print(str(e))


# Load phone use model
phone_use_path_224 = "./models/phone_use_224"
phone_use_model_224 = keras.models.load_model(phone_use_path_224)


# Functions for phone use
def detect_phone_use(path):
    # Dit is een manier om 1 foto in te laden, spijtig genoeg doet hij dan een verkeerde predict???
    # predict_image = keras.preprocessing.image.load_img(path)
    # input_arr = keras.preprocessing.image.img_to_array(predict_image)
    # input_arr = np.array([input_arr])  # Convert single image to a batch.
    # pred_244 = phone_use_model_244.predict(input_array)

    driver_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    driver_generator_224 = driver_datagen.flow_from_directory('./cropped/',
                                                target_size=(224, 224),
                                                color_mode='rgb',
                                                batch_size=1,
                                                class_mode=None,
                                                shuffle=False)

    pred_224 = phone_use_model_224.predict(driver_generator_224, driver_generator_224.n//driver_generator_224.batch_size+1)
    basename = os.path.basename(path)
    os.remove(f'./cropped/driver/{basename}')

    class_pred_224 = np.argmax(pred_224, axis=1)
    return class_pred_224


def predict(path):
    # basename
    basename = os.path.basename(path)

    detect_driver(path)
    prediction = detect_phone_use(f'./cropped/{basename}')

    return prediction


