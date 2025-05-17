# PokemonShinyBot

**PokemonShinyBot** is an automated shiny hunting tool for Pokémon games, currently built specifically for **HeartGold**, **SoulSilver**, and **Platinum**. It features a user-friendly GUI, various customizable settings, and image recognition logic to assist in the shiny hunting process.

> ⚠️ Future support for additional Pokémon titles is in development.

---

## 🚀 Features

- 🖱️ Easy-to-use GUI for configuring shiny hunts
- 🎮 Works with emulators running at **1920x1080 resolution**
- 🔍 Adjustable confidence thresholds for image recognition
- 📜 Logs and feedback for encounters and detection
- 🧪 Includes internal support for:
  - **Wild encounters** (via GUI)
  - **Soft reset hunts** (in codebase)
  - **Starter hunts** (in codebase)

---

## 🛠️ Usage

1. **Clone the repo or download the ZIP**:
   ```bash
   git clone https://github.com/jnotsknab/PokemonShinyBot.git
   ```

2. **Navigate to the project folder**:
   ```bash
   cd PokemonShinyBot
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Open MelonDS & Boot compatible game of choice**:
   ```cd MelonDS or wherever your melonDS path is.
   ```

5. **Run the bot**:
   ```bash
   python shinybot.py
   ```


---

## ⚙️ GUI & Settings

- The bot is optimized for `1920x1080` displays.
- You can customize resolution-specific behavior in the GUI settings.
- Adjust **image recognition confidence values** in case images aren’t being detected properly.

---

## 💡 Useful Info

- The GUI currently supports **wild encounters** only.
- Functions for **soft resetting** and **starter hunting** exist in the codebase.
  - Developers are welcome to expand GUI access to these.
- Contributions and suggestions are always welcome!

---

## 🧪 Dependencies

Ensure Python 3.7+ is installed.

Main packages include:
- `pyautogui`
- `opencv-python`
- `tkinter` (builtin)
- `Pillow`
- `keyboard`

(See `requirements.txt` for full list.)

---

## 📬 Feedback

If you have any issues, suggestions, or contributions, feel free to open an issue or pull request on the [GitHub repo](https://github.com/jnotsknab/PokemonShinyBot).

---

## 📜 License

This project is for educational and entertainment purposes only and is not affiliated with Nintendo or Game Freak.