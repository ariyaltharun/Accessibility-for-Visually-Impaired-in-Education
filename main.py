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


def listen() -> str | None:
    logging.info("Listen Function")
    with sr.Microphone() as source:
        logging.info("Say something")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            logging.info(f"Text to speech: {recognizer.recognize_google(audio)}")
            logging.info("Done")
            return str(recognizer.recognize_google(audio))
        except sr.WaitTimeoutError:
            logging.error("Timeout, please press the button and speak again")
        except sr.UnknownValueError:
            logging.error("Couldn't listen properly")
        except sr.RequestError as e:
            logging.error("Error calling Google Speech Recognition service; {0}".format(e))


def speak(system_text) -> None:
    if system_text:
        mp3_buffer = BytesIO()
        audio = gTTS(system_text)
        audio.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(mp3_buffer, "mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick()


def actions(user_text) -> None:
    global exit
    # while True:
    # User selects the choices
    # user_selection = user_text.value.decode()
    if not user_text:
        return
    
    if "record lectures" in user_text:
        # TODO: Record Lectures function
        # Start recording the lectures by activating certain devices e.g,. microphone
        # Give a name to the lecture
        # Store in a database
        speak("Started Recording Lectures")
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
    elif "minimick scribe" in user_text:
        # TODO: scribe function
        speak("Started Acting as a scribe")
        pass
    elif "exit" in user_text:
        speak("Program exiting")
        exit = True
        pass


# def take_input():
#     global button_click
#     button_click = int(input("Enter 1 to turn mic on or 0 to turn mic off\n").strip())

def main() -> None:
    global exit
    global button_click

    # thread = Thread(target=take_input)
    # thread.start()

    while not exit:
        button_click = int(input("Enter 1 to turn mic on or 0 to turn mic off\n").strip())

        if button_click:
            user_text = listen()
            system_text = actions(user_text)
            speak(system_text)

            button_click = False
        

if __name__ == "__main__":
    main()
