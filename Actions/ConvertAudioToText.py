from gtts import gTTS
from io import BytesIO
import logging
import pygame
import speech_recognition as sr


logging.basicConfig(level=logging.NOTSET, format="[ %(levelname)s ] %(message)s")


recognizer = sr.Recognizer()


user_text: str = None
system_text: str = None
button_click: bool = False
exit: bool = False


def main() -> None:
    global exit
    global button_click

    # thread = Thread(target=take_input)
    # thread.start()

    while not exit:
        button_click = int(input("Enter 1 to convert audio to text:\n").strip())

        if button_click==0:
            exit
        elif button_click:
            r = sr.Recognizer()

            file_audio = sr.AudioFile('RecordedLectures\output.wav')

            with file_audio as source:
                audio_text = r.record(source)

            print(type(audio_text))
            print(r.recognize_google(audio_text))

            with open("recognizedSpeech/new_file.txt", "w") as file:
                file.write(r.recognize_google(audio_text))

            button_click = False
        

if __name__ == "__main__":
    main()