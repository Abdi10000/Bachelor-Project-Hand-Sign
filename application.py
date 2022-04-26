from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import handTrackingModule
import speak
import threading

# den endelige program med koden

# koden fra gtts, siger error og viser fejl
# når der ikke er forbindelse til internettet

# her importerer vi kode fra filen handTrackingModule.py
hand = handTrackingModule

# her importerer vi kode fra filen speak.py
speech = speak

class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        # Grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 1

        # Create a Submit Button
        self.submit = Button(text="Aktiver appen", font_size=32)

        # Bind the Button
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)


        # Create a Speech-to-text button
        self.button = Button(text="Aktiver stemmegenkendelse", font_size=32)

        # Bind the Button
        self.button.bind(on_press=self.pressSound)
        self.add_widget(self.button)



    # funktion for når du trykker på knappen
    # så vil handsign-to-speech blive brugt
    def press(self, instance):
        print('Handsign translation is activated')
        self.add_widget(Label(text=f'Welcome to Hogwarts'))
        hand.main()

        # her hvor der står koden hand.main() er langsom og derfor skal der tilføjes threading
        # vi mangler en exit knap
        # der mangler at koble filen speak.py
        # tilføj en start/main menu

    # funktion for når du trykker på knappen
    # så vil speech-to-text blive brugt
    def pressSound(self, instance):
        print("Speech-to-text transcription is activated")
        self.add_widget(Label(text=f'Is the function working'))
        speech.main()


class TestApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    TestApp().run()