import speech_recognition as sr

# koden her virker
# benyt google recognizer i stedet for pyttsx3

# voice recognition speech-to-text kode

r = sr.Recognizer()

with sr.Microphone() as source:

    print("You can speak now:")

    # read the audio data from the default microphone
    audio_data = r.record(source, duration=5)
    print("Recognizing...")

    # convert speech to text
    text = r.recognize_google(audio_data, language="da-DK")
    print(text)