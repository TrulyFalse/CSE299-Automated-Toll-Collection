import cv2
import numpy as np

# module functions

def grayscale_and_binarize(image_path, output_path, threshold=128):
    # Reads the image and converts it to grayscale simultaneously
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to binarize the image
    binarized_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Save the binarized image
    cv2.imwrite(output_path, binarized_image)

    print(f"Image converted to grayscale and binarized. Saved as {output_path}")

def OCR(image_path):
    vehicle_plate_number = "foo"
    return vehicle_plate_number

def is_registered(vehicle_plate_number):
    is_registered = True;
    return is_registered

def has_payed(vehicle_plate_number):
    has_payed = True;
    return has_payed;