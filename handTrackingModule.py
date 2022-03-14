import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
from gtts import gTTS
from playsound import playsound
import time
import threading
from threading import Thread

# udskift pyttsx3 ud med gtts


# ret projekt og få ordnet tingene i dette program
# når koden er redigeret indsæt pyttsx3

# en alternativ ide kunne være at
# hvis jeg vælger at inddrage gTTS
# i stedet for pyttsx3 som er lort
# så der hvor knoglerne har en if-statement
# så indsæt den gemte lyd fil
# i stedet for at konstant gemme en ny lyd fil
# det var min fejl med at bruge gTTS
# derefter smid lydfilerne på en mappe
# hvor de kan trækkes derfra
# derfor skal jeg kombinere mit
# gamle projekt fra IDS og koble den sammen
# med gTTS

engine = pyttsx3.init()


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


    def handsFinder(self, image, draw=True):
        imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image


    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            if draw:
                cv.circle(image, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        return lmlist

# denne her del af koden skal redigeres
def voice(engine):
    engine.say("Hello")
    engine.runAndWait()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def main():
    cap = cv.VideoCapture(0)
    tracker = handTracker()
    folderPath = "C:/Users/Abdi/Downloads/DivingHandSigns/DivingHandSigns"
    myList = os.listdir(folderPath)
    #print(myList)

    overlayList = []
    for imagePath in myList:
        image = cv.imread(f'{folderPath}/{imagePath}')
        overlayList.append(image)
        #print(len(overlayList))
        detector = handTracker(detectionCon=0.75)

    while True:
        success, image = cap.read()
        image = tracker.handsFinder(image)
        image = cv.flip(image, 1)
        lmList = tracker.positionFinder(image)

        image [0:120, 0:120] = overlayList[0]

        if len(lmList) != 0:

            # The "Thumbs up/Closed fist" statement

            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image [0:120, 0:120] = overlayList[0]
                # print("Thumbs up/Closed fist")
                #engine.say("Thumbs up")
                #engine.runAndWait()
                #voice("Thumbs up")

                #mytext = "Thumbs up"
                #language = 'en'
                #myobj = gTTS(text=mytext, lang=language, slow=False)
                #myobj.save("thumbsup.mp3")
                #os.system("thumbsup.mp3")
                #playsound("C:/Users/Abdi/welcome.mp3")

                speech = "Thumbs up"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # The "OK sign" statement

            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image [0:120, 0:120] = overlayList[1]
                # print("OK sign")
                #engine.say("Ok sign")
                #engine.runAndWait()
                #playsound("")
                #voice("Ok sign")

                speech = "Ok sign"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # The "Stop sign" statement

            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image [0:120, 0:120] = overlayList[2]
                # print("Stop sign")
                #engine.say("Stop sign")
                #engine.runAndWait()
                #playsound("")
                #voice("Stop sign")

                speech = "Stop sign"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # peace sign

            #if lmList[8][2]  lmList[6][2] and lmList[12][2]  lmList[10][2] and lmList[16][2]  lmList[14][2] and lmList[20][2]  lmList[18][2]:
                #image [0:120, 0:120] = overlayList[3]
                # print("Peace sign")
                #engine.say("Peace sign")
                #engine.runAndWait()
                #voice("Peace sign")

        cv.imshow("Video", image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # denne her while loop skal afsluttes med noget destruktion
    engine.stop()
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()