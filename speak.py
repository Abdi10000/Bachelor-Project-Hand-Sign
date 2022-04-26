import speech_recognition as sr

# koden her virker
# benyt google recognizer i stedet for pyttsx3

# voice recognition speech-to-text kode
# tilføj int(input()) til duration

#userInput = input("Hello what is your name: ")

#print(userInput)


# print("how long will you record the person")
# input()
# The record length will be, userInput

def main():

    #print("How long will you record the person?")
    #speechTime = int(input())
    #print("The record duration will be ", speechTime, " seconds")
    #print(type(speechTime))

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("You can speak now:")

        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        #audio_data = r.record(source, duration=int(input()))
        print("Recognizing...")

        # convert speech to text
        text = r.recognize_google(audio_data, language="da-DK")
        print(text)


if __name__ == "__main__":
    main()