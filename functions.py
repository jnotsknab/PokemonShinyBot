import pyautogui as pg
import time
import keyboard
import win32api
import win32con
import numpy as np
import cv2
from PIL import Image
import os
import pygetwindow as gw
import sshgshinyhunter


color_gender_bounds = (0, 268, 270, 53)
colorless_gender_bounds = (0, 268, 270, 53)
locate_image_func_bounds = (0, 530, 1920, 530)
pokemon_ss_bounds = (340, 435, 225, 225)
stop_print_coords = False
pre_loaded_images = {}

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def pre_load_images():
    """
    Pre-loads images to be used in the gender detection function.
    """
    pre_loaded_images['colorlessmale'] = Image.open('images/colorlessmale.png')
    pre_loaded_images['colorlessfemale'] = Image.open('images/colorlessfemale.png')
    pre_loaded_images['male'] = Image.open('images/male.png')
    pre_loaded_images['female'] = Image.open('images/female.png')

pre_load_images()

def clear_images(image_folder='images'):
    """
    Clears all images in the specifed folder.
    """
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def locate_image_boundless(image_path, confidence=0.8):
    """
    Locates the image on the screen without any region restrictions.
    Slower than locate_image function, but will be necessary until the region logic is refactored to support all resolutions.
    """
    try:
        return pg.locateCenterOnScreen(image_path, confidence=confidence)
    except pg.ImageNotFoundException:
        return None


def locate_image(image_path, confidence=0.8, region=locate_image_func_bounds):
    """
    Locates the image on the screen within the specified region.
    """
    try:
        return pg.locateCenterOnScreen(image_path, confidence=confidence, region=region)
    except pg.ImageNotFoundException:
        return None
    


def print_coords():
    """
    Prints the coordinates of the cursor to the console.
    """
    global stop_print_coords
    while not stop_print_coords:
        x, y = pg.position()
        print(f"x: {x}, y: {y}")
        time.sleep(3)
    stop_print_coords = False

def calculate_bounds(x1, y1, x2, y2):
    """
    Calculates bounds based of two x and y coordinates.
    """
    left = x1
    top = y1
    width = x2 - x1
    height = y2 - y1
    bounds = (left, top, width, height)
    print(f'Calculated bounds are: {bounds}')
    return bounds


def take_screenshot(img_name, folder_path='images', region=pokemon_ss_bounds):
    pg.screenshot(f'{folder_path}/{img_name}.png', region=region)

def compare_images(image1, image2, threshold):
    """
    Used in checking shiny for starters, otherwise this function is not used as it is not accurate for wild encounters.
    The arg threshold is the percentage of difference allowed between the two images, for example 0.1 allows for a 10 percent difference.
    """
    if image1 is None or image2 is None:
        return False
    # Compare two images pixel by pixel
    diff_pixels = np.sum(np.abs(np.array(image1) - np.array(image2)))
    total_pixels = image1.shape[0] * image1.shape[1] * image1.shape[2]
    difference_percentage = diff_pixels / total_pixels

    if difference_percentage <= threshold:
        return True
    else:
        return False

def compare_images_with_rgb(img1, img2, threshold=0):
    """
    Compares two images pixel by pixel with RGB values.
    The threshold arg represents the percent of difference allowed between the two images allowed, for example threshold=7 is a 7 percent differene allowed.
    """
    img1_pil = Image.fromarray(img1)
    img2_pil = Image.fromarray(img2)
    
    img1_rgb = img1_pil.convert('RGB')
    img2_rgb = img2_pil.convert('RGB')

    diff_percentage = calculate_image_difference(img1_rgb, img2_rgb)

    return diff_percentage <= threshold

def calculate_image_difference(img1, img2):
    '''
    Calculates the percentage difference between two images and returns the value calculated.
    '''
    img1_array = np.array(img1)
    img2_array = np.array(img2)

    diff = np.abs(img1_array - img2_array)

    # Calculate mean absolute difference
    mean_diff = np.mean(diff)

    # Calculate percentage difference based on image size
    num_pixels = img1_array.shape[0] * img1_array.shape[1] * img1_array.shape[2]
    diff_percentage = (mean_diff / 255) * 100 

    return diff_percentage

def detect_gender():
    """
    Detects the gender of the pokemon on the screen by using image recognition to locate the gender symbol in the nameplate.
    If none of the predefined gender images are found we assume the pokemon is genderless.
    """
    female = locate_image(pre_loaded_images['female'], confidence=0.85, region=color_gender_bounds)
    male = locate_image(pre_loaded_images['male'], confidence=0.85, region=color_gender_bounds)
    colorless_male = locate_image('images/colorlessmale.png', confidence=0.85, region=colorless_gender_bounds)
    colorless_female = locate_image('images/colorlessfemale.png', confidence=0.85, region=colorless_gender_bounds)
    if female or colorless_female:
        print('female')
        return 'female'
    elif male or colorless_male:
        print('male')
        return 'male'
    elif not (male or female or colorless_male or colorless_female):
        print('genderless')
        return 'genderless'
    else:
        return None


def is_image_black(image):
    return np.all(image == 0)

def get_focused_window_title():
    """
    Get the title of the focused window.
    """
    focused_window = gw.getWindowsWithTitle(gw.getActiveWindowTitle())
    if focused_window:
        return focused_window[0].title
    else:
        return None

