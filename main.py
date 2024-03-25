import logging
from time import sleep
import speech_recognition as sr
import streamlit as st

from utils import listen, speak
from Actions.LectureManager import record_lectures, replay_lecture
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
        sleep(0.5)
        speak("Tell the file name")
        user_response: str = listen()
        replay_lecture(user_response.replace(" ", "_"))
        pass
    elif "act as scribe" in user_text.lower():
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

    button = st.button(label="On Microphone")

    if button:
        speak("How can I help you?")
        user_text = listen()
        system_text = actions(user_text)
        speak(system_text)


if __name__ == "__main__":
    main()
