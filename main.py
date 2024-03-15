import logging
from time import sleep
import speech_recognition as sr

from utils import listen, speak
from Actions.RecordLectures import record_lectures
from Actions.Scribe import scribe


logging.basicConfig(level=logging.NOTSET, format="[ %(levelname)s ] %(message)s")


recognizer = sr.Recognizer()


user_text: str = None
system_text: str = None
button_click: bool = False
exit: bool = False


def actions(user_text) -> None:
    global exit
    if not user_text:
        return
    
    if "record lectures" in user_text:
        # TODO: Record Lectures function
        # Start recording the lectures by activating certain devices e.g,. microphone
        # Give a name to the lecture
        # Store in a database
        speak("Started Recording Lectures")
        speak("What would you name this lecture?")
        filename = listen()
        speak(f"{filename} name is cool")
        filename = filename.replace(" ", "_") + ".wav"
        record_lectures(filename)
        pass
    elif "replay lectures" in user_text:
        # TODO: replay Lectures function
        # Search a lecture based on user_query(name of lecture) in the database
        # Play the lecture
        speak("Started Replaying Lectures")
        pass
    elif "summarize lecture" in user_text:
        # TODO: summarize Lectures function
        speak("Started Summarizing lecture")
        pass
    elif "act as scribe" in user_text:
        # TODO: scribe function
        speak("Started Acting as a scribe")
        sleep(1)
        scribe()
        pass
    elif "exit" in user_text:
        speak("Program exiting")
        exit = True
        pass


def main() -> None:
    global exit
    global button_click

    while not exit:
        button_click = int(input("Enter 1 to turn mic on or 0 to turn mic off\n").strip())

        if button_click:
            user_text = listen()
            system_text = actions(user_text)
            speak(system_text)

            button_click = False
        

if __name__ == "__main__":
    main()
