import customtkinter as ctk
from pynput import keyboard
from PIL import ImageGrab
import easyocr
import os
import threading
from ai_req import query_custom_gpt

# Global variables to track the state
is_window_open = False
is_hotkey_active = True

def read_screenshot(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path, paragraph=True)
    recognized_text = " ".join([detection[1] for detection in results])
    return recognized_text

def process_screen_content(callback):
    screenshot = ImageGrab.grab()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    screen_content_str = read_screenshot(screenshot_path)
    callback(screen_content_str)


def on_submit(entry, submit_button, response_label, root, screen_content, event=None):
    user_input = entry.get()
    print("Input Submitted:", user_input)

    # Call the ai_req function with OCR result and user input
    gpt_response = query_custom_gpt(screen_content, user_input)
    print("GPT-3 Response:", gpt_response)

    # Update the GUI with the GPT-3 response
    response_label.configure(text=gpt_response)
    response_label.pack(pady=10)
    root.geometry("400x300")  # Adjusted height to 300
    submit_button.configure(state='disabled')

def update_after_ocr(entry, submit_button, response_label, root, screen_content):
    # Print the OCR result to the console
    print("OCR Result:", screen_content)

    # Enable the submit button
    submit_button.configure(state='normal')

    # Set the command of the submit button and Enter key binding
    submit_action = lambda: on_submit(entry, submit_button, response_label, root, screen_content)
    submit_button.configure(command=submit_action)
    root.bind('<Return>', lambda event: submit_action())

def on_close(root):
    global is_window_open, is_hotkey_active
    is_window_open = False
    is_hotkey_active = True  # Reset the hotkey activation
    print(f"Waiting for new input {is_hotkey_active}")
    root.destroy()

def on_activate():
    global is_window_open, is_hotkey_active

    if is_window_open or not is_hotkey_active:
        return

    is_window_open = True
    is_hotkey_active = False

    root = ctk.CTk()
    root.title("ScreenGPT")
    window_width, window_height = 400, 100
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    center_x, center_y = int(screen_width / 2), int(screen_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.attributes('-topmost', True)

    entry = ctk.CTkEntry(root, width=300)
    entry.pack(pady=10)

    submit_button = ctk.CTkButton(root, text="Submit", state='disabled')  # Initially disabled
    submit_button.pack(pady=10)

    response_label = ctk.CTkLabel(root, text="", wraplength=window_width - 20)
    response_label.pack(pady=10)  # Pack it initially

    ocr_thread = threading.Thread(target=process_screen_content, args=(
    lambda content: root.after(0, update_after_ocr, entry, submit_button, response_label, root, content),))
    ocr_thread.start()

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()

def for_canonical(f):
    listener = keyboard.Listener(on_press=lambda k: k)
    return lambda k: f(listener.canonical(k))

read_screenshot('./screenshot.png')

print("Listening for ctrl + u ...")

hotkey = keyboard.HotKey(
    {keyboard.Key.ctrl, keyboard.KeyCode.from_char('u')},
    on_activate)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as listener:
    listener.join()
