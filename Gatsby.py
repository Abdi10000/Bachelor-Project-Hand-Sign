# Programmet er udviklet af Projektgruppen:
# Medlemmerne består af Abdi, Michael og Kristina.
# Dato 01/06-2022
# Koden oversætter hånd tegn til lyd


# Dependencies for Gatsby prototypen
import cv2 as cv
import mediapipe as mp
import os
import pyttsx3
import threading


# variablen for outputting lyd
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


# højtaler funktionen til at omdanne tekst til lyd
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Threading funktion der gør at koden kører uden afbrydelser
def fasterCode(input, argument):
    handling = threading.Thread(target=input, args=(argument,))
    handling.start()


def main():

    # Webkameraets størrelse på skærmen
    webcamWidth = 1200
    webcamHeight = 800

    #
    webcam = cv.VideoCapture(0)

    # Adjusting the webcam width and height
    webcam.set(cv.CAP_PROP_FRAME_WIDTH, webcamWidth)
    webcam.set(cv.CAP_PROP_FRAME_HEIGHT, webcamHeight)


    # variablen for at anvende handTracker class
    tracker = handTracker()
    folderPath = "Pictures"
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


        #
        if len(lmList) != 0:

            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image[0:120, 0:120] = overlayList[0]
                speech = "Hello"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image[0:120, 0:120] = overlayList[1]
                speech = "Goodbye"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image[0:120, 0:120] = overlayList[2]
                speech = "Thank you"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image[0:120, 0:120] = overlayList[3]
                speech = "Can you help me"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image[0:120, 0:120] = overlayList[4]
                speech = "I want to buy"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image[0:120, 0:120] = overlayList[5]
                speech = "How do i find"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] > lmList[18][2]:
                image[0:120, 0:120] = overlayList[6]
                speech = "I am deaf"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image[0:120, 0:120] = overlayList[7]
                speech = "Can you repeat"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image[0:120, 0:120] = overlayList[8]
                speech = "okay"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


            #
            if lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2]:
                image[0:120, 0:120] = overlayList[9]
                speech = "stop"
                cv.putText(image, speech, (0, 400), cv.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 4, cv.LINE_AA)
                fasterCode(speak, speech)


        cv.imshow("Tegnsprog applikation", image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    engine.stop()
    webcam.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()