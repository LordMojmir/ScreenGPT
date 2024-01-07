import pyttsx3

def text_to_speech(text):
    try:
        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Convert the text to speech
        engine.say(text)

        # Wait for the speech to finish
        engine.runAndWait()
        engine.stop()
        return True
    except Exception as e:
        # You can optionally print the error or handle it differently
        print(f"An error occurred: {e}")
        return False

# Example usage
# result = text_to_speech("   Hello, this is a test.")
# print("Success:", result)
