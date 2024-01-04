import customtkinter as ctk
from pynput import keyboard
from PIL import ImageGrab
import easyocr
import os
from ai_req import query_custom_gpt

def read_screenshot(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    recognized_text = " ".join([detection[1] for detection in results])
    return recognized_text

def process_screen_content():
    screenshot = ImageGrab.grab()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    screen_content_str = read_screenshot(screenshot_path)
    return screen_content_str

def on_submit(entry, submit_button, response_label, root, screen_content):
    user_input = entry.get()
    print("Input Submitted:", user_input)
    gpt_response = query_custom_gpt(screen_content, user_input)
    print("GPT-3 Response:", gpt_response)

    # Update the GUI with the GPT-3 response and resize the window
    response_label.configure(text=gpt_response)
    response_label.pack(pady=10)

    # Resize the window to fit the response label
    root.geometry("400x300")  # Adjusted height to 300

    # Disable the submit button
    submit_button.configure(state='disabled')

def on_activate():
    screen_content_str = process_screen_content()
    print("Screen content:", screen_content_str)

    root = ctk.CTk()
    root.title("Input")

    window_width = 400
    window_height = 100  # Initial height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    entry = ctk.CTkEntry(root, width=300)
    entry.pack(pady=10)

    submit_button = ctk.CTkButton(root, text="Submit")
    submit_button.pack(pady=10)

    response_label = ctk.CTkLabel(root, text="", wraplength=window_width-20)

    # Set the command of the submit button
    submit_button.configure(command=lambda: on_submit(entry, submit_button, response_label, root, screen_content_str))

    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    root.mainloop()

def for_canonical(f):
    listener = keyboard.Listener(on_press=lambda k: k)
    return lambda k: f(listener.canonical(k))

print("Listening for hotkey...")

hotkey = keyboard.HotKey(
    {keyboard.Key.ctrl, keyboard.KeyCode.from_char('h')}, # , keyboard.KeyCode.from_char('m')
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    listener.join()
