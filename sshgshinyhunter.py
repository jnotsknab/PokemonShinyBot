import pyautogui as pg
import time
import keyboard
import numpy as np
from PIL import Image
from functions import *
import numpy as np
import threading
import pygame
import pytesseract
import os
import cv2
import pickle
from changetime import set_system_time


pygame.init()
shiny_sound = pygame.mixer.Sound('sfx/shiny_sound.mp3')
no_shiny_sound = pygame.mixer.Sound('sfx/no_shiny.mp3')
pk_mon_positions = ((1190, 272), (1680, 292))
move_positions = ((1200, 365), (1685, 365))
pre_loaded_images = {}
start_from_count = 0
general_confidence = 0.8
shiny_icon_confidence = 0.9
pokemon_database = {}
speed_thread = None
stop_shiny_hunt = False

def pre_load_images():
    pre_loaded_images['sys'] = Image.open('images/sys.png')
    pre_loaded_images['reset'] = Image.open('images/reset.png')
    # pre_loaded_images['cyn'] = Image.open('images/cyn.png')
    # pre_loaded_images['tot'] = Image.open('images/tot.png')
    # pre_loaded_images['chik'] = Image.open('images/chik.png')
    pre_loaded_images['fight'] = Image.open('images/fight.png')
    pre_loaded_images['run'] = Image.open('images/run.png')
    pre_loaded_images['pktotrade'] = Image.open('images/pktotrade.png')
    pre_loaded_images['pkball'] = Image.open('images/pkball.png')
    pre_loaded_images['summary'] = Image.open('images/summary.png')
    pre_loaded_images['abra'] = Image.open('images/abra.png')
    pre_loaded_images['shiny'] = Image.open('images/shiny.png')
    pre_loaded_images['swifty'] = Image.open('images/swifty.png')
    pre_loaded_images['switchpk'] = Image.open('images/switchpk.png')
    pre_loaded_images['pokemonbtn'] = Image.open('images/pokemonbtn.png')
    pre_loaded_images['dratini'] = Image.open('images/dratininameplate.png')
    pre_loaded_images['purchasedratini'] = Image.open('images/purchasedratini.png')

def soft_reset(sleep_time):
    """
    Soft resets the game by using image recognition to locate the system button and the reset button.
    """
    time.sleep(sleep_time)
    sys_pos = locate_image_boundless(pre_loaded_images['sys'], confidence=general_confidence)
    if sys_pos:
        click(sys_pos.x, sys_pos.y)
        time.sleep(sleep_time - sleep_time*0.8)
        reset_pos = locate_image_boundless(pre_loaded_images['reset'], confidence=general_confidence)
        if reset_pos:
            click(reset_pos.x, reset_pos.y)
    else:
        print('System button not found, cannot execute soft reset...')

def load_reset_count(start_from):
    """
    Loads the reset count from the pickle file if it exists, otherwise returns the start_from value (should be 0).
    """
    if os.path.exists("reset_count.pkl"):
        with open("reset_count.pkl", "rb") as file:
            return pickle.load(file)
    else:
        return start_from

def save_reset_count(reset_count):
    """
    Updates the reset count in the pickle file.
    """
    with open("reset_count.pkl", "wb") as file:
        pickle.dump(reset_count, file)

def check_shiny_starters(sleep_time=0.75):
    """
    Will not work for now as the base images for the starters are not in the images folder.
    """
    # speed_thread = threading.Thread(target=speed_up_emu_thread)
    # speed_thread.start()
    # print('Speeding up emulator...')

    print('Shiny checking starting in 5 seconds...')
    time.sleep(5)
    base_cyn_img, base_tot_img, base_chik_img = pre_loaded_images['cyn'], pre_loaded_images['tot'], pre_loaded_images['chik']
    shiny_found: bool = False
    while not keyboard.is_pressed('q') and not shiny_found:

        take_screenshot('potential_chik_shiny')
        potential_chik_shiny = Image.open('images/potential_chik_shiny.png')

        if not compare_images(base_chik_img, potential_chik_shiny):
            print('Chik is shiny!')
            shiny_found = True
            shiny_sound.play()
            break

        keyboard.press('d')
        time.sleep(0.1)
        keyboard.release('d')

        time.sleep(sleep_time)

        take_screenshot('potential_tot_shiny')
        potential_tot_shiny = Image.open('images/potential_tot_shiny.png')

        if not compare_images(base_tot_img, potential_tot_shiny):
            print('Tot is shiny!')
            shiny_found = True
            shiny_sound.play()
            break
        
        keyboard.press('d')
        time.sleep(0.1)
        keyboard.release('d')

        time.sleep(sleep_time)

        take_screenshot('potential_cyn_shiny')
        potential_cyn_shiny = Image.open('images/potential_cyn_shiny.png')
        if not compare_images(base_cyn_img, potential_cyn_shiny):
            print('Cyn is shiny!')
            shiny_found = True
            shiny_sound.play()
            break

        else:
            print('No shiny found...')
            no_shiny_sound.play()
            # keyboard.press('d')
            # time.sleep(0.1)
            # keyboard.release('d')
            # time.sleep(sleep_time)
            soft_reset(sleep_time)
            time.sleep(2.5)
            for _ in range(5):
                keyboard.press('x')
                time.sleep(0.1)
                keyboard.release('x')

def check_shiny_sr(sleep_time):
    print(f'shiny hunting starting in {sleep_time} seconds...')
    time.sleep(sleep_time)
    try:
        with open("reset_count.txt", "r") as file:
            reset_count = int(file.read())
    except FileNotFoundError:
        reset_count = 0
    
    # speed_thread = threading.Thread(target=speed_up_emu_thread)
    # speed_thread.start()
    shiny_found = False
    sr_bounds = (625, 425, 300, 280)
    time.sleep(2.5)
    for _ in range(2):
        keyboard.press('x')
        time.sleep(0.1)
        keyboard.release('x')
        time.sleep(0.25)
    for _ in range(4):
        while True:
            purchase_pos = locate_image_boundless(pre_loaded_images['purchasedratini'], confidence=general_confidence)
            if purchase_pos:
                click(purchase_pos.x, purchase_pos.y)
                time.sleep(0.2)
                keyboard.press('x')
                time.sleep(0.05)
                keyboard.release('x')
                break
        time.sleep(0.25)
        keyboard.press('x')
        time.sleep(0.1)
        keyboard.release('x')
    for _ in range(4):
        keyboard.press('c')
        time.sleep(0.1)
        keyboard.release('c')
        time.sleep(0.25)
    
    while True:
        pk_ball = locate_image_boundless(pre_loaded_images['pkball'], confidence=general_confidence)
        if pk_ball:
            click(pk_ball.x, pk_ball.y)
            break
    # time.sleep(0.75)
    while True:
        pk_to_check_pos = locate_image_boundless(pre_loaded_images['dratini'], confidence=general_confidence)
        if pk_to_check_pos:
            click(pk_to_check_pos.x, pk_to_check_pos.y)
            break
    while True:
        summary_pos = locate_image_boundless(pre_loaded_images['summary'], confidence=general_confidence)
        if summary_pos:
            click(summary_pos.x, summary_pos.y)
            break
    time.sleep(0.75)
    for _ in range(5):
        time.sleep(0.33)
        shiny_pos = locate_image_boundless(pre_loaded_images['shiny'], confidence=shiny_icon_confidence)
        if shiny_pos:
            shiny_sound.play()
            print(f'Shiny found! in {reset_count} resets.')
            shiny_found = True
            break
        else:
            keyboard.press('s')
            time.sleep(0.03)
            keyboard.release('s')
            print(f'No shiny found... in reset number {reset_count}...')
            no_shiny_sound.play()
        # take_screenshot('base_pk_sr_img', region=sr_bounds)

    while not keyboard.is_pressed('q') and not shiny_found:
        soft_reset(0.2)
        reset_count += 1
        time.sleep(2.5)
        for _ in range(7):
            keyboard.press('x')
            time.sleep(0.1)
            keyboard.release('x')
            time.sleep(0.25)
        for _ in range(4):
            while True:
                purchase_pos = locate_image_boundless(pre_loaded_images['purchasedratini'], confidence=general_confidence)
                if purchase_pos:
                    click(purchase_pos.x, purchase_pos.y)
                    time.sleep(0.2)
                    keyboard.press('x')
                    time.sleep(0.05)
                    keyboard.release('x')
                    break
            time.sleep(0.25)
            keyboard.press('x')
            time.sleep(0.1)
            keyboard.release('x')
        for _ in range(4):
            keyboard.press('c')
            time.sleep(0.1)
            keyboard.release('c')
            time.sleep(0.25)

        # time.sleep(0.5)
        while True:
            pk_ball = locate_image_boundless(pre_loaded_images['pkball'], confidence=general_confidence)
            if pk_ball:
                click(pk_ball.x, pk_ball.y)
                break
                
        # time.sleep(0.75)
        while True:
            pk_to_check_pos = locate_image_boundless(pre_loaded_images['dratini'], confidence=general_confidence)
            if pk_to_check_pos:
                click(pk_to_check_pos.x, pk_to_check_pos.y)
                break
        while True:
            summary_pos = locate_image_boundless(pre_loaded_images['summary'], confidence=general_confidence)
            if summary_pos:
                click(summary_pos.x, summary_pos.y)
                break
        time.sleep(0.75)
        for _ in range(5):
            time.sleep(0.25)  # Wait for 2 seconds before proceeding to the next iteration
            shiny_pos = locate_image_boundless(pre_loaded_images['shiny'], confidence=shiny_icon_confidence)
            if shiny_pos:
                shiny_sound.play()
                print(f'Shiny found! in {reset_count} resets.')
                shiny_found = True
                break
            else:
                keyboard.press('s')
                time.sleep(0.03)
                keyboard.release('s')
                print(f'No shiny found... in reset number {reset_count}...')
                no_shiny_sound.play()

def wild_shiny():
    """
    Shiny hunts for wild pokemon in Heartgold and Soulsilver.
    Note that the image recognition will flag false positives if the game happens to transition from day to night etc, as the background colors will chage.
    To avoid this I've added a function that sets the system time to a specific date and time.
    Setting the system time requires admin priveleges, so the script will need to be run as an administrator.
    If the user wishes this feature can be disabled to avoid the need for admin priveleges, but you will need to be careful to avoid false positives for when the gamestate transitions from day to night.
    """
    # Load existing database if available
    try:

        global speed_thread, stop_shiny_hunt
        if os.path.exists("pokemon_database.pkl"):
            with open("pokemon_database.pkl", "rb") as file:
                pokemon_database = pickle.load(file)
        else:
            pokemon_database = {}

        reset_count = load_reset_count(start_from_count)
        new_encounter_img = cv2.imread('wildimages/base_pk_img.png')
        nameplate_bounds = (0, 268, 245, 53)
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        shiny_found = False
        print('Shiny hunting starting in 5 seconds, make sure you tab into the emulator for the window to be recognized...')
        print(f'Starting from reset number {reset_count}...')
        print(f'General confidence level: {general_confidence}, Shiny icon confidence level: {shiny_icon_confidence}, edit in settings if images arent being detected...')
        time.sleep(5)
        while not shiny_found and not stop_shiny_hunt:
            entered_battle = locate_image_boundless(pre_loaded_images['fight'], confidence=general_confidence)
            focused_window = get_focused_window_title()
            if focused_window is not None:

                if not entered_battle and 'melonDS' in focused_window:
                    keyboard.press('d')
                    time.sleep(0.01)
                    keyboard.release('d')
                    time.sleep(0.01)
                    keyboard.press('a')
                    time.sleep(0.01)
                    keyboard.release('a')
                    time.sleep(0.01)
                    keyboard.press('d')
                    time.sleep(0.01)
                    keyboard.release('d')
                    time.sleep(0.01)
                    keyboard.press('a')
                    time.sleep(0.01)
                    keyboard.release('a')
                elif 'melonDS' not in focused_window:
                    print('melonDS window not in focus, waiting for focus...')
                    time.sleep(1)
                else:
                    print('Entered battle...')
                    reset_count += 1
                    take_screenshot('nameplate', region=nameplate_bounds, folder_path='wildimages')
                    gender = detect_gender()
                    name_plate_img = None
                    # give the image time to be saved before reading it
                    while name_plate_img is None:
                        name_plate_img = cv2.imread('wildimages/nameplate.png')
                    name_plate_text = pytesseract.image_to_string(name_plate_img, config=custom_config).strip()
                    # modify the nameplate text to match the key in the database
                    if gender == 'female':
                        name_plate_text += '_female'
                    elif gender == 'genderless':
                        name_plate_text += '_genderless'
                    print("Nameplate Text:", name_plate_text)

                    if name_plate_text in pokemon_database:
                        print(f'{name_plate_text} already in the database. Comparing colors to check if shiny...')
                        if gender == 'female':
                            saved_color_img = pokemon_database[name_plate_text]['female_color']
                        elif gender == 'genderless':
                            saved_color_img = pokemon_database[name_plate_text]['color']
                        else:
                            saved_color_img = pokemon_database[name_plate_text]['male_color']

                        entered_battle = locate_image_boundless(pre_loaded_images['fight'], confidence=general_confidence)
                        if entered_battle:
                            take_screenshot('base_pk_img', region=(600, 316, 250, 205), folder_path='wildimages')
                        new_encounter_img_path = 'wildimages/base_pk_img.png'
                        saved_img_path = f'wildimages/{name_plate_text}_{"female" if gender == "female" else "genderless" if gender == "genderless" else "male"}_pk.png'
                        new_encounter_img = cv2.imread('wildimages/base_pk_img.png')
                        print(f'Comparing colors for {saved_img_path} and {new_encounter_img_path}...')
                        if not compare_images_with_rgb(saved_color_img, new_encounter_img, threshold=7):
                            reset_count_db = 'reset_count.pkl'
                            if os.path.exists(reset_count_db):
                                os.remove(reset_count_db)
                            shiny_sound.play()
                            print(f"Shiny found! {name_plate_text} is shiny!")
                            shiny_found = True
                            print(f'Shiny found in {reset_count} resets.')
                            break
                        else:
                            print(f"{name_plate_text}is not a shiny, reset number {reset_count}...")
                            no_shiny_sound.play()
                            run_pos = locate_image_boundless(pre_loaded_images['run'], confidence=general_confidence)
                            if run_pos:
                                click(run_pos.x, run_pos.y)
            

                    else:
                        #new encounter, the saved img for the mon will be the same as the new encounter img
                        take_screenshot('base_pk_img', region=(600, 316, 250, 205), folder_path='wildimages')
                        print(f"New Pokémon {name_plate_text} encountered. Adding to the database.")
                        run_pos = locate_image_boundless(pre_loaded_images['run'], confidence=general_confidence)
                        if run_pos:
                            click(run_pos.x, run_pos.y)
                        saved_color_img = cv2.imread('wildimages/base_pk_img.png')
                        #save the base image for the mon to the database
                        if gender == 'female':
                            pokemon_database[name_plate_text] = {'female_color': saved_color_img}
                        elif gender == 'genderless':
                            pokemon_database[name_plate_text] = {'color': saved_color_img}
                        else:
                            pokemon_database[name_plate_text] = {'male_color': saved_color_img}
                        
                        try:
                            if gender == 'genderless':
                                os.rename('wildimages/nameplate.png', f"wildimages/{name_plate_text}_nameplate.png")
                                os.rename('wildimages/base_pk_img.png', f"wildimages/{name_plate_text}_pk.png")
                                print("Genderless Pokémon files renamed successfully.")
                                print("Images smoothed successfully.")
                            else:
                                os.rename('wildimages/nameplate.png', f"wildimages/{name_plate_text}_{gender}_nameplate.png")
                                os.rename('wildimages/base_pk_img.png', f"wildimages/{name_plate_text}_{gender}_pk.png")
                                print(f"Files renamed successfully for gender {gender}...")
                                print("Images smoothed successfully.")
                        except Exception as e:
                            print("Error renaming files:", e)

        # Save the database to folder
        with open("pokemon_database.pkl", "wb") as file:
            pickle.dump(pokemon_database, file)
        save_reset_count(reset_count)
    except Exception as e:
        print(f"Error occurred: {e}")

#call this function to initialize the images that are utilized throughout the script.
pre_load_images()
# time.sleep(3)
# wild_shiny(0.75)








