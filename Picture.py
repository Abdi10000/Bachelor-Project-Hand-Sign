# Kivy dependencies
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout


# Prototype dependencies
import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
import threading
import speech_recognition as sr


# variable for outputting the audio
engine = pyttsx3.init()


# en klasse der bruges til at opfange hånden ved brug af mediapipe
class handTracker():
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

    # funktion der beregner og viser positioner på fingre
    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            if draw:
                # cv.circle skal fjernes
                cv.circle(image, (cx, cy), 4, (255, 205, 195), cv.FILLED)
                #cv.rectangle(image, (h, w), (300, 300), (0, 255, 255), cv.FILLED)

        return lmlist


# højtaler funktionen
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Build app and layout
class CampApp(App):

    def build(self):
        # Main layout components
        self.image = Image(size_hint=(1, .8))
        #self.speech = Label(text="hello", size_hint=(1, .1))

        # Add items to layout
        global layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.image)
        #layout.add_widget(self.speech)


        # Setup video capture device
        # The size of webcamera screen
        self.capture = cv.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)


        # variablen for at anvende handTracker class
        global tracker
        tracker = handTracker()


        # Hvad er %(source.dir)s/Pictures

        # denne her path skal ændres når den indsættes på appen
        folderPath = "C:/Users/Abdi/PycharmProjects/pythonProject/Pictures"
        #folderPath = "Pictures"
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


        # Speech-to-text button
        self.voiceButton = Button(text="Speech-To-Text Button", size_hint=(1,.1))




        # Bind the Button
        self.voiceButton.bind(on_press=self.pressVoice)
        layout.add_widget(self.voiceButton)

        # koderne nedenunder virker ikke
        #handleVoice = threading.Thread(target=pressVoice, args=(,)
        #handleVoice.start()


        # Exit button
        self.exitButton = Button(text="Exit Button", font_size=32, size_hint=(1,.1), background_color=(1, 0, 0, 1))

        # Bind the Button
        self.exitButton.bind(on_press=self.pressExit)
        layout.add_widget(self.exitButton)


        # Label for speech-to-text


        return layout

        # funktion for når du trykker på knappen
        # så vil du exit appen


    def pressExit(self, instance):
        #self.background_color = (1, 0, 1, 1)  # skal måske fjernes
        #self.add_widget(Label(text="The app is shutting down"))
        layout.add_widget(Label(text="The app is shutting down"))
        CampApp.stop()
        # tilføj ja/nej funktion


    # koden her skal sikkert placeres i sit eget fil
    # dvs. importer koden fra filen kaldet speak.py


    # fix threading på denne funktion
    # function for speech-to-text
    def pressVoice(self, instance):
        layout.add_widget(Label(text="Speech-to-text transcription is activated"))
        print("Speech-to-text transcription is activated")
        layout.add_widget(Label(text="You can speak now:"))

        # s = input("Enter the time in seconds: ")

        r = sr.Recognizer()

        with sr.Microphone() as source:
            #layout.add_widget(Label(text="You can speak now:"))
            print("You can speak now:")

            # makes sure outside sound are not contaminating the voice recognition
            r.adjust_for_ambient_noise(source)

            try:
                # read the audio data from the microphone
                # records the user. the user can choose the length/duration

                # audio_data = r.record(source, duration=int(s))
                audio_data = r.record(source, duration=10)
                print("Recognizing...")
                #self.add_widget(Label(text="Recognizing..."))
                layout.add_widget(Label(text="Recognizing..."))

                # listens for the user's input
                # programming stops when user stops talking
                # audio = r.listen(source)
                #audio = r.listen(audio_data)

                # convert speech to text
                # text = r.recognize_google(audio_data, language="da-DK")
                global textSpeech
                textSpeech = r.recognize_google(audio_data, language="da-DK")
                print(textSpeech)
                #self.add_widget(Label(text=textSpeech))
                layout.add_widget(Label(text=textSpeech))

                # tilføj label tekst herunder
                #self.add_widget(Label(text=textSpeech))

                #handleVoice = threading.Thread(target=pressVoice, args=(,))
                #handleVoice.start()


            # måske skal den her error fjernes
            except sr.RequestError:
                print("Voice was not recognized")
                #self.add_widget(Label(text="Voice was not recognized"))
                layout.add_widget(Label(text="Voice was not recognized"))


            except sr.UnknownValueError:
                print("Error")
                #self.add_widget(Label(text="Error"))
                layout.add_widget(Label(text="Error"))



    # Run continuously to get webcam feed
    def update(self, *args):

        # Read frame from opencv
        ret, frame = self.capture.read()

        frame = cv.flip(frame, 1)

        self.image_frame = frame


        track = tracker.handsFinder(frame)
        # Flip horizontal and convert image to texture
        buffer = cv.flip(frame, 0).tostring()
        texture = Texture.create(size=(track.shape[1], track.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture
        #cv.putText(frame, "hello", (400, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)


        # flips the camera and makes sure that the webcam is not inverted(spejlvendt)
        #image = cv.flip(image, 1)

        #
        lmList = tracker.positionFinder(track)

        #
        if len(lmList) != 0:

            # Lukket hånd
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[0]
                speech = "Hello"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[1]
                speech = "Goodbye"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[2]
                speech = "Thank you"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[3]
                speech = "Can you help me"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[4]
                speech = "I want to buy"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[5]
                speech = "How do i find"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[6]
                speech = "I am deaf"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[7]
                speech = "Can you repeat"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[8]
                speech = "okay"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[9]
                speech = "stop"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()



if __name__ == '__main__':
    app = CampApp()
    app.run()

    #CampApp().run()


# funktion til at konverter fra image/opencv til kivy
def convert(insert):
    buffer = "hello"
    print(buffer)
    print(insert)
    print("This function is not active")


    # hvad sker der hvis koden buffer = cv.flip(frame, 0).tostring() bliver fjernet
    # vi har fjernet tommelfinger i vores program, da det er problematisk at arbejde med det
    # tilføj ja/nej funktion når man skal gå ud af appen
