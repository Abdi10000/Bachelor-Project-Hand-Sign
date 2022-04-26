import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
import threading
from gtts import gTTS

# husk at ændre det engelske til dansk
# husk at forklare koden grundigt
# det kan være at programmet skal indlæse håndtegn hurtigere
# husk også at fjerne den der pink cirkel
# udskift pyttsx3 med gTTS



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
                cv.circle(image, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        return lmlist


# højtaler funktionen
def speak(audio):
    engine.say(audio)
    engine.runAndWait()




def main():

    # The size of webcamera screen
    webcamWidth = 1200
    webcamHeight = 800

    webcam = cv.VideoCapture(0)

    # Adjusting the webcam width and height
    webcam.set(cv.CAP_PROP_FRAME_WIDTH, webcamWidth)
    webcam.set(cv.CAP_PROP_FRAME_HEIGHT, webcamHeight)

    # variablen for at anvende handTracker class
    tracker = handTracker()
    folderPath = "C:/Users/Abdi/Downloads/DivingHandSigns/DivingHandSigns"
    myList = os.listdir(folderPath)
    #print(myList)

    # denne array indeholder listen af hånd tegn billeder
    overlayList = []
    for imagePath in myList:
        image = cv.imread(f'{folderPath}/{imagePath}')
        overlayList.append(image)
        #print(len(overlayList))
        detector = handTracker(detectionCon=0.75)


    # A while loop which/that is handling webcam screen continuation
    while True:

        #
        success, image = webcam.read()

        #
        image = tracker.handsFinder(image)

        # flips the camera and makes sure that the webcam is not inverted(spejlvendt)
        image = cv.flip(image, 1)

        #
        lmList = tracker.positionFinder(image)

        # jeg behøver ikke koden nedenunder
        #image [0:120, 0:120] = overlayList[0]

        #
        if len(lmList) != 0:

            # The "Thumbs up statement

            if lmList[4][2] < lmList[3][2] and lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image [0:120, 0:120] = overlayList[0]

                speech = "Thumbs up"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # The "OK sign" statement
            # ok sign skal sikkert slettes fordi
            # den følger ikke billedet korrekt

            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image [0:120, 0:120] = overlayList[1]

                speech = "Ok"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # The "Hej sign" statement

            if lmList[4][2] < lmList[3][2] and lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image [0:120, 0:120] = overlayList[2]

                speech = "Hej"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # peace sign

            if lmList[4][2] > lmList[3][2] and lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                #image [0:120, 0:120] = overlayList[]

                speech = "Peace";
                # fred
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # tilføj ja håndtegn
            if lmList[4][2] > lmList[3][2] and lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                # image [0:120, 0:120] = overlayList[]

                speech = "ja"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            # tilføj nej håndtegn
            if lmList[4][2] < lmList[3][2] and lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                # image [0:120, 0:120] = overlayList[]

                speech = "nej"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


            #if lmList[8][2] > lmList[5][2]

            if lmList[4][2] > lmList[3][2] and lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                #image [0:120, 0:120] = overlayList[]

                speech = "Pneumonoultramicroscopicsilicovolcanoconiosis"
                t_handle = threading.Thread(target=speak, args=(speech,))
                t_handle.start()


        cv.imshow("Tegnsprog applikation", image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # denne her while loop skal afsluttes med noget destruktion
    engine.stop()
    webcam.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()