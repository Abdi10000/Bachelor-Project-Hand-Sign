# Programmet er udviklet af Projektgruppen:
# Medlemmerne består af Abdi, Michael og Kristina
# Dato 01/06-2022

# Koden er en applikation der indeholder funktioner
# for at brugeren kan holde en samtale
# den inkludere oversættelse af håndtegn til tale
# og optagelse af stemme der transskriberes til tekst


# Kivy dependencies
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture


# Prototypen Fiesta dependencies
import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
import threading
import speech_recognition as sr


# variablen for outputting the audio
engine = pyttsx3.init()


# en klasse der bruges til at opfange hånden ved brug af mediapipe
class handTracker():

    # en funktion der bruges til at opfange hånden ved brug af mediapipe
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplexity = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    # funktion der tegner og finder hånden
    def handsFinder(self, image, draw=True):
        imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image


    # funktion der beregner og viser positioner på hånden
    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            if draw:
                cv.circle(image, (cx, cy), 4, (255, 205, 195), cv.FILLED)

        return lmlist


# højtaler funktionen
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# funktion for threading
# Threading funktion der gør at koden kører uden afbrydelser
def fasterCode(input, argument):
    handling = threading.Thread(target=input, args=(argument,))
    handling.start()






class MainApp(App):

    def build(self):

        global layout
        layout = BoxLayout(orientation='vertical')

        self.image = Image(size_hint=(1, .8))

        layout.add_widget(self.image)


        self.capture = cv.VideoCapture(0)
        Clock.schedule_interval(self.signTracking, 1.0 / 33.0)


        # Speech-to-text button
        self.voiceButton = Button(text="Speech-To-Text Button", size_hint=(1,.1))

        # Bind the Speech-To-Text Button
        self.voiceButton.bind(on_press=self.pressVoice)
        layout.add_widget(self.voiceButton)


        # Exit button
        self.exitButton = Button(text="Exit Button", font_size=32, size_hint=(1,.1), background_color=(1, 0, 0, 1))

        # Bind the Exit Button
        self.exitButton.bind(on_press=self.pressExit)
        layout.add_widget(self.exitButton)


        # variablen for at anvende handTracker class
        global tracker
        tracker = handTracker()

        # kode der fører til filen med billeder
        folderPath = "Pictures"
        myList = os.listdir(folderPath)
        # print(myList)


        # denne array indeholder listen af hånd tegn billeder
        global overlayList
        overlayList = []
        for imagePath in myList:
            image = cv.imread(f'{folderPath}/{imagePath}')
            overlayList.append(image)
            # print(len(overlayList))
            detector = handTracker(detectionCon=0.75)

        return layout


    # funktion for når du trykker på knappen
    # så vil du exit appen
    def pressExit(self, instance):
        layout.add_widget(Label(text="The app is shutting down"))
        MainApp.stop()



    # funktion for speech-to-text
    def pressVoice(self, instance):

        print("Speech-to-text transcription is activated")
        layout.add_widget(Label(text="Speech-to-text transcription is activated"))
        layout.add_widget(Label(text="You can speak now:"))


        r = sr.Recognizer()


        with sr.Microphone() as source:
            print("You can speak now:")
            layout.add_widget(Label(text="You can speak now:"))

            # Denne linje kode gør at andre lyde ikke påvirker stemmegenkendelse
            r.adjust_for_ambient_noise(source)

            try:
                # read the audio data from the microphone
                # records the user. the user can choose the length/duration
                audio = r.record(source, duration=10)
                print("Recognizing...")
                layout.add_widget(Label(text="Recognizing..."))

                # Konverterer tale til tekst
                global textSpeech
                textSpeech = r.recognize_google(audio, language="da-DK")
                print(textSpeech)
                layout.add_widget(Label(text=textSpeech))



            except sr.RequestError:
                print("Voice was not recognized")
                #self.add_widget(Label(text="Voice was not recognized"))
                layout.add_widget(Label(text="Voice was not recognized"))



            except sr.UnknownValueError:
                print("Error")
                layout.add_widget(Label(text="Error"))



    # Denne funktion bruges til at kombinere OpenCV med Kivy
    def signTracking(self, *args):


        ret, frame = self.capture.read()

        # Flipper webkameraet
        frame = cv.flip(frame, 1)


        self.image_frame = frame


        track = tracker.handsFinder(frame)

        # Konverter image til texture
        buffer = cv.flip(frame, 0).tostring()
        texture = Texture.create(size=(track.shape[1], track.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


        lmList = tracker.positionFinder(track)


        if len(lmList) != 0:


            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[0]
                speech = "Hello"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[1]
                speech = "Goodbye"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[2]
                speech = "Thank you"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[3]
                speech = "Can you help me"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[4]
                speech = "I want to buy"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)


            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[5]
                speech = "How do i find"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[6]
                speech = "I am deaf"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[7]
                speech = "Can you repeat"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[8]
                speech = "okay"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)



            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[9]
                speech = "stop"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)


if __name__ == '__main__':
    app = MainApp()
    app.run()