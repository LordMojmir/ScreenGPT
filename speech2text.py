import speech_recognition as sr

def listen_continuously():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Continuously listen and transcribe
        while True:
            try:
                # Adjust the recognizer sensitivity to ambient noise
                r.adjust_for_ambient_noise(source, duration=1)

                # Listen for the first phrase and extract it into audio data
                audio = r.listen(source)

                # Recognize speech using Google Web Speech API
                text = r.recognize_google(audio)
                print(f"I heard: {text}")
                return text
            except sr.UnknownValueError:
                print("I could not understand audio")
                return "I could not understand audio"
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def listen_for_input() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            # Listen for the first phrase and extract it into audio data
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            # Recognize speech using Google Web Speech API
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "I could not understand audio"
        except sr.RequestError:
            return "Could not request results; check your internet connection"
        except sr.WaitTimeoutError:
            return "No speech was detected within the time limit"

# Run the continuous listening function
# listen_continuously()

# print(listen_for_input())