# A line used mostly as the first one, imports App class
# that is used to get a window and launch the application
from kivy.app import App

# Casual Kivy widgets that reside in kivy.uix
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition


# Kivy dependencies
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture


from kivy.uix.popup import Popup

from kivy.uix.image import Image
from kivy.clock import Clock
import cv2 as cv


# Prototypen Fiesta dependencies
import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
import threading
import speech_recognition as sr
from kivy.uix.textinput import TextInput

from gtts import gTTS
from io import BytesIO
import pyglet
import playsound
import threading
import pyaudio
import speech_recognition as sr
import cv2 as cv
import mediapipe as mp
import os



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



class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        #layout.add_widget(Label(text='main screen', size_hint_y=0.2))
        layout.add_widget(Label(text='Velkommen til Fiesta appen', size_hint_y=0.2))


        layout.add_widget(Image(source="10.png"))


        # Add another layout to handle the navigation
        # and set the height of navigation to 20%
        # of the CustomScreen
        navig = BoxLayout(size_hint_y=0.2)

        # Create buttons with a custom text
        prev = Button(text='Previous')
        next = Button(text='Next')
        exit = Button(text='Exit', background_color='#FFA500', size_hint_y=0.2)

        # Bind to 'on_release' events of Buttons
        prev.bind(on_release=self.switch_prev)
        next.bind(on_release=self.switch_next)
        exit.bind(on_release=self.pressExit)

        # Add buttons to navigation
        # and the navigation to layout
        navig.add_widget(prev)
        navig.add_widget(next)
        layout.add_widget(navig)
        layout.add_widget(exit)

        # And add the layout to the Screen
        self.add_widget(layout)

        # *args is used to catch arguments that are returned
        # when 'on_release' event is dispatched

    def switch_prev(self, *args):
        # 'self.manager' holds a reference to ScreenManager object
        # and 'ScreenManager.current' is a name of a visible Screen
        # Methods 'ScreenManager.previous()' and 'ScreenManager.next()'
        # return a string of a previous/next Screen's name
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.previous()

        # tilføj i stedet mod handsign-to-speech
        # self.manager.current = Maybe

    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()



    #
    def pressExit(self, instance):

        self.popWindow(self)


    #
    def popWindow(self, *args):

        self.textpopup(title='Exit', text='Are you sure?')
        return True


    #
    def textpopup(self, title='', text=''):


        """Open the pop-up with the name.

        :param title: title of the pop-up to open
        :type title: str
        :param text: main text of the pop-up to open
        :type text: str
        :rtype: None
        """

        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))

        mybutton = Button(text='Yes', size_hint=(1, 1))
        box.add_widget(mybutton)

        otherbutton = Button(text='No', size_hint=(1, 1))
        box.add_widget(otherbutton)


        popup = Popup(title=title, content=box, size_hint=(None, None), size=(600, 300))
        #mybutton.bind(on_release=ScreenManagerApp.stop(self))
        mybutton.bind(on_release=self.stop)
        otherbutton.bind(on_release=popup.dismiss)
        popup.open()


    def stop(self, instance):
        ScreenManagerApp.stop(self)



class HandToSpeech(Screen):

    def __init__(self, **kwargs):
        super(HandToSpeech, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        #layout.add_widget(Label(text='hand-to-speech screen'))


        # camera
        self.image = Image(size_hint=(1, .8))
        layout.add_widget(self.image)
        self.capture = cv.VideoCapture(0)
        Clock.schedule_interval(self.signTracking, 1.0 / 33.0)


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
            #detector = handTracker(detectionCon=0.75)


        # Add another layout to handle the navigation
        # and set the height of navigation to 20%
        # of the CustomScreen
        navig = BoxLayout(size_hint_y=0.2)

        # Create buttons with a custom text
        prev = Button(text='Previous')
        next = Button(text='Next')
        exit = Button(text='Exit', background_color='#FFA500', size_hint_y=0.2)

        # Bind to 'on_release' events of Buttons
        prev.bind(on_release=self.switch_prev)
        next.bind(on_release=self.switch_next)
        exit.bind(on_release=self.pressExit)

        # Add buttons to navigation
        # and the navigation to layout
        navig.add_widget(prev)
        navig.add_widget(next)
        layout.add_widget(navig)
        layout.add_widget(exit)

        # And add the layout to the Screen
        self.add_widget(layout)

        # *args is used to catch arguments that are returned
        # when 'on_release' event is dispatched

    # tilføj for if-statement condition disable i denne funktion
    def switch_prev(self, *args):
        # 'self.manager' holds a reference to ScreenManager object
        # and 'ScreenManager.current' is a name of a visible Screen
        # Methods 'ScreenManager.previous()' and 'ScreenManager.next()'
        # return a string of a previous/next Screen's name
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.previous()


        # et forsøg på at skabe conditions for at disable handsign-to-speech
        #if self.manager.current == self.manager.previous:
        #    print("Prut")
        #    class HandToSpeech = disabled(True)


    # tilføj for if-statement condition disable i denne funktion
    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()



    #
    def pressExit(self, instance):

        self.popWindow(self)


    #
    def popWindow(self, *args):

        self.textpopup(title='Exit', text='Are you sure?')
        return True


    #
    def textpopup(self, title='', text=''):


        """Open the pop-up with the name.

        :param title: title of the pop-up to open
        :type title: str
        :param text: main text of the pop-up to open
        :type text: str
        :rtype: None
        """

        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))

        mybutton = Button(text='Yes', size_hint=(1, 1))
        box.add_widget(mybutton)

        otherbutton = Button(text='No', size_hint=(1, 1))
        box.add_widget(otherbutton)


        popup = Popup(title=title, content=box, size_hint=(None, None), size=(600, 300))
        #mybutton.bind(on_release=ScreenManagerApp.stop(self))
        mybutton.bind(on_release=self.stop)
        otherbutton.bind(on_release=popup.dismiss)
        popup.open()


    def stop(self, instance):
        ScreenManagerApp.stop(self)


    # Denne funktion bruges til at kombinere OpenCV med Kivy
    def signTracking(self, *args):


        ret, frame = self.capture.read()

        # Flipper webkameraet
        frame = cv.flip(frame, 1)


        #self.image_frame = frame


        track = tracker.handsFinder(frame)

        # Konverter image til texture
        buffer = cv.flip(frame, 0).tostring()
        texture = Texture.create(size=(track.shape[1], track.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


        lmList = tracker.positionFinder(track)


        if len(lmList) != 0:


            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve
            # så vil programmet output ordet "hello" fra højtaleren
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[0]
                speech = "Hello"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)


            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover pegefingeren
            # så vil programmet output ordet "goodbye" fra højtaleren
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[1]
                speech = "Goodbye"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)

            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover pegefingeren
            # og langfingeren så vil programmet output sætningen "thank you" fra højtaleren
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[2]
                speech = "Thank you"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)

            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover pegefingeren
            # mellemfineren og ringefingeren så vil programmet output sætningen "Can you help me" fra højtaleren
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[3]
                speech = "Can you help me"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)


            # Denne if-statement gør at når brugerens fire fingre er foldet ud
            # så vil programmet output sætningen "I want to buy" fra højtaleren
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[4]
                speech = "I want to buy"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)


            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover pegefingeren
            # og lillefingeren så vil programmet output sætningen "How do i find" fra højtaleren
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[5]
                speech = "How do i find"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)

            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover mellemfingeren
            # og ringfingeren så vil programmet output sætningen "I am deaf" fra højtaleren
            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                frame[0:120, 0:120] = overlayList[6]
                speech = "I am deaf"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)

            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover lillefingeren
            # så vil programmet output sætningen "Can you repeat" fra højtaleren
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[7]
                speech = "Can you repeat"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)

            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover pegefingeren,
            # ringfingeren og lillefingeren så vil programmet output ordet "okay" fra højtaleren
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[8]
                speech = "Okay"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

                fasterCode(speak, speech)

            # Denne if-statement gør at når brugerens hånd er foldet til en knytnæve udover mellemfingeren,
            # ringfingeren og lillefingeren så vil programmet output ordet "Stop" fra højtaleren
            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                frame[0:120, 0:120] = overlayList[9]
                speech = "Stop"

                alphabet = cv.putText(frame, speech, (0, 450), cv.FONT_HERSHEY_SIMPLEX, 2, (25, 255, 255), 4, lineType=cv.LINE_AA)

                buffer = cv.flip(alphabet, 0).tostring()
                texture = Texture.create(size=(alphabet.shape[1], alphabet.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture


                # kode der skal afprøves
                #convert(alphabet)


                fasterCode(speak, speech)



class TextToSpeech(Screen):

    def __init__(self, **kwargs):
        super(TextToSpeech, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')


        # Code only focusing on text-to-speech:
        # Label widget
        self.voicing = Label(text="What are you gonna type?", font_size=18, color='#00FFCE')
        layout.add_widget(self.voicing)

        # text input widget for text-to-speech
        self.texting = TextInput(multiline=False)
        layout.add_widget(self.texting)

        # text-to-speech button
        self.textSpeech = Button(text="text-to-speech button")
        self.textSpeech.bind(on_press=self.speak)
        layout.add_widget(self.textSpeech)


        # tilføj previous, next og exit knap

        # Add another layout to handle the navigation
        # and set the height of navigation to 20%
        # of the CustomScreen
        navig = BoxLayout(size_hint_y=0.2)

        # Create buttons with a custom text
        prev = Button(text='Previous')
        next = Button(text='Next')
        exit = Button(text='Exit', background_color='#FFA500', size_hint_y=0.2)

        # Bind to 'on_release' events of Buttons
        prev.bind(on_release=self.switch_prev)
        next.bind(on_release=self.switch_next)
        exit.bind(on_release=self.pressExit)

        # Add buttons to navigation
        # and the navigation to layout
        navig.add_widget(prev)
        navig.add_widget(next)
        layout.add_widget(navig)
        layout.add_widget(exit)

        # And add the layout to the Screen
        self.add_widget(layout)

        # *args is used to catch arguments that are returned
        # when 'on_release' event is dispatched

    def switch_prev(self, *args):
        # 'self.manager' holds a reference to ScreenManager object
        # and 'ScreenManager.current' is a name of a visible Screen
        # Methods 'ScreenManager.previous()' and 'ScreenManager.next()'
        # return a string of a previous/next Screen's name
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.previous()

        # tilføj i stedet mod handsign-to-speech
        # self.manager.current = Maybe

    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()



    # function for text-to-speech
    def speak(self, instance):


        if not self.texting.text:

            self.voicing.text = 'Fejl, du mangler at skrive i feltet'
            self.texting.text = ''


        else:


            # text for testing
            self.voicing.text = self.texting.text

            # converting sound to bytes
            voiceOver = BytesIO()

            # prøv og indsæt threading
            tts = gTTS(text=self.texting.text, lang='da', slow=False)
            tts.write_to_fp(voiceOver)
            voiceOver.seek(0)

            # her indsæt threading
            test = pyglet.media.load(None, file=voiceOver, streaming=False)
            test.play()

            #
            # pyglet.app.run()

            #
            # playsound(test)

            self.texting.text = ''


    #
    def pressExit(self, instance):

        self.popWindow(self)


    #
    def popWindow(self, *args):

        self.textpopup(title='Exit', text='Are you sure?')
        return True


    #
    def textpopup(self, title='', text=''):


        """Open the pop-up with the name.

        :param title: title of the pop-up to open
        :type title: str
        :param text: main text of the pop-up to open
        :type text: str
        :rtype: None
        """

        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))

        mybutton = Button(text='Yes', size_hint=(1, 1))
        box.add_widget(mybutton)

        otherbutton = Button(text='No', size_hint=(1, 1))
        box.add_widget(otherbutton)


        popup = Popup(title=title, content=box, size_hint=(None, None), size=(600, 300))
        #mybutton.bind(on_release=ScreenManagerApp.stop(self))
        mybutton.bind(on_release=self.stop)
        otherbutton.bind(on_release=popup.dismiss)
        popup.open()


    def stop(self, instance):
        ScreenManagerApp.stop(self)



class SpeechToText(Screen):

    def __init__(self, **kwargs):
        super(SpeechToText, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Code only focusing on speech-to-text
        self.voiceText = Label(text="Here is the label for speech-to-text", font_size=18, color='#00FFCE')
        layout.add_widget(self.voiceText)

        # speech-to-text button
        self.voiceButton = Button(text="Speech-to-text button", size_hint=(1, 1))
        self.voiceButton.bind(on_press=self.voiceTrend)
        layout.add_widget(self.voiceButton)


        # Add another layout to handle the navigation
        # and set the height of navigation to 20%
        # of the CustomScreen
        navig = BoxLayout(size_hint_y=0.2)

        # Create buttons with a custom text
        prev = Button(text='Previous')
        next = Button(text='Next')
        exit = Button(text='Exit', background_color='#FFA500', size_hint_y=0.2)

        # Bind to 'on_release' events of Buttons
        prev.bind(on_release=self.switch_prev)
        next.bind(on_release=self.switch_next)
        exit.bind(on_release=self.pressExit)

        # Add buttons to navigation
        # and the navigation to layout
        navig.add_widget(prev)
        navig.add_widget(next)
        layout.add_widget(navig)
        layout.add_widget(exit)

        # And add the layout to the Screen
        self.add_widget(layout)

        # *args is used to catch arguments that are returned
        # when 'on_release' event is dispatched

    def switch_prev(self, *args):
        # 'self.manager' holds a reference to ScreenManager object
        # and 'ScreenManager.current' is a name of a visible Screen
        # Methods 'ScreenManager.previous()' and 'ScreenManager.next()'
        # return a string of a previous/next Screen's name
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.previous()

        # tilføj i stedet mod handsign-to-speech
        # self.manager.current = Maybe

    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()


    #
    def pressExit(self, instance):

        self.popWindow(self)


    #
    def popWindow(self, *args):

        self.textpopup(title='Exit', text='Are you sure?')
        return True


    #
    def textpopup(self, title='', text=''):


        """Open the pop-up with the name.

        :param title: title of the pop-up to open
        :type title: str
        :param text: main text of the pop-up to open
        :type text: str
        :rtype: None
        """

        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))

        mybutton = Button(text='Yes', size_hint=(1, 1))
        box.add_widget(mybutton)

        otherbutton = Button(text='No', size_hint=(1, 1))
        box.add_widget(otherbutton)


        popup = Popup(title=title, content=box, size_hint=(None, None), size=(600, 300))
        #mybutton.bind(on_release=ScreenManagerApp.stop(self))
        mybutton.bind(on_release=self.stop)
        otherbutton.bind(on_release=popup.dismiss)
        popup.open()


    def stop(self, instance):
        ScreenManagerApp.stop(self)



    # function for speech-to-text
    def voiceTrend(self, instance):


        self.voiceText.text = "Speech-to-text transcription is activated"

        r = sr.Recognizer()

        #self.voiceText.text = self.


        with sr.Microphone() as source:


            # Denne linje kode gør at andre lyde ikke påvirker stemmegenkendelse
            #r.adjust_for_ambient_noise(source)


            try:

                self.voiceText.text = "You can speak now:"
                #print("You can speak now:")

                # read the audio data from the microphone
                # records the user. the user can choose the length/duration
                audio = r.record(source, duration=10)
                #print("Recognizing...")
                self.voiceText.text = "Recognizing..."


                # Konverterer tale til tekst
                textSpeech = r.recognize_google(audio, language="da-DK")
                #print(textSpeech)
                self.voiceText.text = textSpeech
                #self.voiceText.text = ''


            #
            except sr.RequestError:
                #print("Voice was not recognized")
                self.voiceText.text = "Voice was not recognized"
                #self.voiceText.text = ''


            #
            except sr.UnknownValueError:
                #print("Error")
                self.voiceText.text = "Error"
                #self.voiceText.text = ''


class ScreenManagerApp(App):

    def build(self):
        root = ScreenManager()

        root.add_widget(MainScreen(name='Main'))
        root.add_widget(HandToSpeech(name='Hand'))
        root.add_widget(TextToSpeech(name='Text'))
        root.add_widget(SpeechToText(name='Speech'))

        return root

if __name__ == '__main__':
    ScreenManagerApp().run()