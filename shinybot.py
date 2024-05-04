import sys
import tkinter as tk
import threading
import sshgshinyhunter
import os
import functions
from tkinter import simpledialog
import time

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert("end", str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

class SettingsWindow:
    """
    A class to create a settings window for the user to adjust various settings for the shiny hunting script such as bounds and confidence levels.
    I only have one computer to test this program on, so the user may need to adjust certain settings.
    """
    def __init__(self, parent):
        self.parent = parent
        self.settings_window = tk.Toplevel(parent)
        self.settings_window.title("Settings")
        self.settings_window.geometry("700x400")

        # Add widgets for adjusting settings
        self.general_confidence_label = tk.Label(self.settings_window, text="General Confidence (must be a float between 0 and 1):")
        self.general_confidence_label.grid(row=0, column=0, padx=10, pady=5)
        self.general_confidence_entry = tk.Entry(self.settings_window)
        self.general_confidence_entry.grid(row=0, column=1, padx=10, pady=5)

        self.shiny_icon_confidence_label = tk.Label(self.settings_window, text="Shiny Icon Confidence (must be a float between 0 and 1):")
        self.shiny_icon_confidence_label.grid(row=1, column=0, padx=10, pady=5)
        self.shiny_icon_confidence_entry = tk.Entry(self.settings_window)
        self.shiny_icon_confidence_entry.grid(row=1, column=1, padx=10, pady=5)

        self.pk_ss_label = tk.Label(self.settings_window, text="Pokemon SS Bounds, must be tuple (left, top, width, height):")
        self.pk_ss_label.grid(row=3, column=0, padx=10, pady=5)
        self.pk_ss_entry = tk.Entry(self.settings_window)
        self.pk_ss_entry.grid(row=3, column=1, padx=10, pady=5)

        self.color_gender_bounds_label = tk.Label(self.settings_window, text="Color Gender Bounds, must be tuple (left, top, width, height):")
        self.color_gender_bounds_label.grid(row=4, column=0, padx=10, pady=5)
        self.color_gender_bounds_entry = tk.Entry(self.settings_window)
        self.color_gender_bounds_entry.grid(row=4, column=1, padx=10, pady=5)

        self.colorless_gender_bounds_label = tk.Label(self.settings_window, text="Colorless Gender Bounds, must be tuple (left, top, width, height):")
        self.colorless_gender_bounds_label.grid(row=5, column=0, padx=10, pady=5)
        self.colorless_gender_bounds_entry = tk.Entry(self.settings_window)
        self.colorless_gender_bounds_entry.grid(row=5, column=1, padx=10, pady=5)

        self.save_btn = tk.Button(self.settings_window, text="Save", command=self.save_settings)
        self.save_btn.grid(row=6, columnspan=2, padx=10, pady=5)

    def save_settings(self):
        """
        Saves various settings entered by the user in the settings window
        Once the application closes these settings will be lost, eventually I will add functionality to save these settings to a json file.
        For now I would recommend saving these settings in a text file or something similar/take a picture once the settings you save are output to the text widget.
        """
        try:
            sshgshinyhunter.general_confidence = float(self.general_confidence_entry.get())
            sshgshinyhunter.shiny_icon_confidence = float(self.shiny_icon_confidence_entry.get())
            functions.pokemon_ss_bounds = eval(self.pk_ss_entry.get())
            functions.color_gender_bounds = eval(self.color_gender_bounds_entry.get())
            functions.colorless_gender_bounds = eval(self.colorless_gender_bounds_entry.get())
        except Exception as e:
            print(f"Invalid input: {e}")
            return

        print("General Confidence value saved:", sshgshinyhunter.general_confidence)
        print("Shiny Icon Confidence value saved:", sshgshinyhunter.shiny_icon_confidence)
        print("Pokemon SS Bounds saved:", functions.pokemon_ss_bounds)
        print("Color Gender Bounds saved:", functions.color_gender_bounds)
        print("Colorless Gender Bounds saved:", functions.colorless_gender_bounds)
        self.settings_window.destroy()

class PokemonShinyHuntGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokemon Shiny Hunting Bot")

        self.create_widgets()
        self.initialize_output_redirection()
        self.print_instructions()

    def initialize_output_redirection(self):
        # Redirect stdout and stderr to the Text widget
        sys.stdout = TextRedirector(self.text_widget, "stdout")
        sys.stderr = TextRedirector(self.text_widget, "stderr")


    def print_instructions(self):
        # Clear existing text in the Text widget
        self.text_widget.delete(1.0, tk.END)
        
        # Print instructions to the Text widget
        instructions_text = (
        'The start button will start the shiny hunting process for wild pokemon in Heartgold and Soulsilver (currently working on making other games compatible), must be a wild encounter (grass, cave, building, etc).\n'
        '-------------------------------------------------------------------------------------------------\n'
        'The stop button will stop the shiny hunting process and printing coordinates to the console if it is enabled.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'The settings button will open the settings window, where you can edit the confidence levels for image recognition, along with various bounds, etc.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'The reset encounter count button will reset the encounter count back to 0\n'
        '-------------------------------------------------------------------------------------------------\n'
        'The set time to morning button will set the system time to 7:00 AM, the set time to day button will set the system time to 10:00 AM, and the set time to night button will set the system time to 7:00 PM.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'Setting the system time requires admin priveleges, so if you wish to use it run the executable as administrator.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'False positives WILL occur if the game transitions from day to night, etc while the script is running, so I recommend setting the system time to the specified time for the specific pokemon you are hunting.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'Currently when settings are saved it only updates the variables associated with those values, so if you close the program and reopen it the settings will be reset to the default values.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'I will implement functionality to save to a settings json file in the future, but for now I recommend editing the values in the script or taking a picture of your settings once you have them configured.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'The calculate bounds button will open a dialog to input coordinates to calculate bounds, the bounds are used for image recognition.\n'
        '-------------------------------------------------------------------------------------------------\n'
        'The print mouse coordinates button will print the current x and y coordinates of the cursor to the console every 3 seconds until stop is pressed.\n'
        '-------------------------------------------------------------------------------------------------\n'
    )
        self.text_widget.insert(tk.END, instructions_text)

    def open_coordinate_input_dialog(self):
        """
        Opens a dialog to input coordinates for bound calculation.
        """
        dialog = simpledialog.Toplevel()
        dialog.title("Input Coordinates")

        # Create entry fields for the coordinates
        tk.Label(dialog, text="Top Left X:").grid(row=0, column=0)
        top_left_x_entry = tk.Entry(dialog)
        top_left_x_entry.grid(row=0, column=1)

        tk.Label(dialog, text="Top Left Y:").grid(row=1, column=0)
        top_left_y_entry = tk.Entry(dialog)
        top_left_y_entry.grid(row=1, column=1)

        tk.Label(dialog, text="Bottom Right X:").grid(row=2, column=0)
        bottom_right_x_entry = tk.Entry(dialog)
        bottom_right_x_entry.grid(row=2, column=1)

        tk.Label(dialog, text="Bottom Right Y:").grid(row=3, column=0)
        bottom_right_y_entry = tk.Entry(dialog)
        bottom_right_y_entry.grid(row=3, column=1)

        # Function to pass the coordinates to calculate_bounds
        def calculate_with_coordinates():
            top_left_x = int(top_left_x_entry.get())
            top_left_y = int(top_left_y_entry.get())
            bottom_right_x = int(bottom_right_x_entry.get())
            bottom_right_y = int(bottom_right_y_entry.get())
            functions.calculate_bounds(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
            dialog.destroy()  # Close the dialog window after calculation

        # Button to trigger the calculation with the provided coordinates
        calculate_button = tk.Button(dialog, text="Calculate", command=calculate_with_coordinates)
        calculate_button.grid(row=4, columnspan=2)

    def create_widgets(self):
        # Create a Text widget to display the console output
        self.text_widget = tk.Text(self.master)
        self.text_widget.place(x=10, y=10, width=1875, height=900)

        # Create a Scrollbar and attach it to the Text widget
        scrollbar = tk.Scrollbar(self.master, command=self.text_widget.yview)
        scrollbar.place(x=1885, y=10, height=900)
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Create buttons
        self.coords_btn = tk.Button(self.master, text="Print Mouse Coordinates", command=lambda: threading.Thread(target = functions.print_coords).start())
        self.coords_btn.place(x=25, y=925, width=175, height=50)

        self.calculate_bounds_btn = tk.Button(self.master, text="Calculate Bounds", command=self.open_coordinate_input_dialog)
        self.calculate_bounds_btn.place(x=200, y=925, width=150, height=50)

        self.start_btn = tk.Button(self.master, text="Start", command=self.start_shiny_hunt)
        self.start_btn.place(x=575, y=925, width=100, height=50)

        self.stop_btn = tk.Button(self.master, text="Stop", command=self.stop_shiny_hunt)
        self.stop_btn.place(x=675, y=925, width=100, height=50)

        self.settings_btn = tk.Button(self.master, text="Settings", command=self.open_settings)
        self.settings_btn.place(x=775, y=925, width=100, height=50)

        self.reset_btn = tk.Button(self.master, text="Reset Encounter Count", command=self.reset_encounter_count)
        self.reset_btn.place(x=875, y=925, width=150, height=50)

        self.set_morning_btn = tk.Button(self.master, text="Set Time to Morning", command = lambda: sshgshinyhunter.set_system_time(2024, 5, 4, 7, 0, 0))
        self.set_morning_btn.place(x=1025, y=925, width=150, height=50)

        self.set_day_btn = tk.Button(self.master, text="Set Time to Day", command = lambda: sshgshinyhunter.set_system_time(2024, 5, 4, 10, 0, 0))
        self.set_day_btn.place(x=1175, y=925, width=150, height=50)

        self.set_night_btn = tk.Button(self.master, text="Set Time to Night", command = lambda: sshgshinyhunter.set_system_time(2024, 5, 4, 19, 0, 0))
        self.set_night_btn.place(x=1325, y=925, width=150, height=50)

    def start_shiny_hunt(self):
        # Start the shiny hunt process in a new thread
        threading.Thread(target=sshgshinyhunter.wild_shiny, daemon=True).start()

    def stop_shiny_hunt(self):
        sshgshinyhunter.stop_shiny_hunt = True
        functions.stop_print_coords = True

    def open_settings(self):
        SettingsWindow(self.master)

    def reset_encounter_count(self):
        reset_count_db = 'reset_count.pkl'
        if os.path.exists(reset_count_db):
            print('Encounter count has been reset to 0.')
            os.remove(reset_count_db)
        else:
            print('Encounter count has already been reset, or the file does not exist.')

def main():
    root = tk.Tk()
    PokemonShinyHuntGUI(root)
    root.geometry("1920x1080")
    root.iconbitmap("images/appicon.ico")
    root.wm_iconbitmap("images/appicon.ico")
    root.mainloop()

if __name__ == "__main__":
    main()

