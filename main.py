import customtkinter as ctk
from pynput import keyboard
from PIL import ImageGrab
import easyocr
import ctypes

def on_submit(entry, root):
    input_value = entry.get()
    print("Input Submitted:", input_value)
    root.destroy()

def read_screenshot(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    for detection in result:
        print(detection[1])  # Print the text

def on_activate():
    root = ctk.CTk()
    root.title("Input")

    # Set the window size and position it in the center of the screen
    window_width = 400
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Create a wider input field
    entry = ctk.CTkEntry(root, width=300)
    entry.pack(pady=10)

    submit_button = ctk.CTkButton(root, text="Submit", command=lambda: on_submit(entry, root))
    submit_button.pack(pady=10)

    root.mainloop()

    screenshot = ImageGrab.grab()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)

    read_screenshot(screenshot_path)

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    {keyboard.Key.ctrl, keyboard.KeyCode.from_char('s'), keyboard.KeyCode.from_char('m')},
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
