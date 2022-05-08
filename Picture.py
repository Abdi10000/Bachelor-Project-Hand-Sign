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


# OpenCV dependencies
import cv2 as cv
import tensorflow as tf
import os
import numpy as np

import handTrackingModule


import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
import threading
import application
from kivy.uix.label import Label

from gtts import gTTS
from io import BytesIO
import pyglet
from playsound import playsound



# variable for outputting the audio
engine = pyttsx3.init()

# converting sound to bytes
voiceOver = BytesIO()


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
                cv.circle(image, (cx, cy), 15, (255, 0, 255), cv.FILLED)
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
        #self.button = Button(text="Verify", size_hint=(1,.1))
        #self.verification = Label(text="Verification Uninitialized", size_hint=(1,.1))

        # Add items to layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.image)
        #layout.add_widget(self.button)
        #layout.add_widget(self.verification)


        # Setup video capture device
        # The size of webcamera screen
        self.capture = cv.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)


        # variablen for at anvende handTracker class
        global tracker
        tracker = handTracker()
        folderPath = "C:/Users/Abdi/Downloads/Hands/HandSignList"
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


        # Exit button
        self.exitButton = Button(text="Exit Button", font_size=32, size_hint=(1,.1), background_color=(1, 0, 0, 1))

        # Bind the Button
        self.exitButton.bind(on_press=self.pressExit)
        layout.add_widget(self.exitButton)

        # tilføj tilbage knap
        #self.backButton = Button(text="Back Button", size_hint=(1,.1))

        # Bind the Button
        #self.backButton.bind(on_press=self.pressBack)
        #layout.add_widget(self.backButton)

        return layout

        # funktion for når du trykker på knappen
        # så vil du exit appen


    def pressExit(self, instance):
        # print("Exit knap aktiveret")
        self.background_color = (1, 0, 1, 1)  # skal måske fjernes
        CampApp.stop()


    #def pressBack(self, instance):
    #    print("The button works")
        # knappen mangler at blive tilføjet
        # byt knappen ud med speech-to-text



    # Run continuously to get webcam feed
    def update(self, *args):

        # Read frame from opencv
        ret, frame = self.capture.read()

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

            # Lukket hånd - 0 - Done -
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[0]
                speech = "Hey"

                buffer = cv.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # Ja - 1 - Done -
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[1]
                speech = "Yes"

                buffer = cv.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # Nej - 2 - Done -
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[2]
                speech = "No"

                buffer = cv.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # Måske - 3 - Done -
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[3]
                speech = "Maybe"

                buffer = cv.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # Hvad hedder du - 4 - Done -
            #if lmList[0][2] > lmList[1][2] and
            #if lmList[0][2] < lmList[1][2] and

            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[4]
                speech = "What is your name?"

                buffer = cv.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # billedet skal skiftes ud. Men hånd tegnen virker
            # Farvel - 5 - Done - Den virker
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[5]
                speech = "Goodbye"

                buffer = cv.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()
                #cv.rectangle(frame, (100, 100), (300, 300), (0, 255, 255), cv.FILLED)
                #cv.putText(frame, speech, (400, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)


            #tilføj flere fingrer kommandoer

            # Ord?
            #if lmList


if __name__ == '__main__':
    CampApp().run()