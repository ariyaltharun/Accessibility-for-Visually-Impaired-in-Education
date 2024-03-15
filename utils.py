import logging
import speech_recognition as sr
import pygame
from gtts import gTTS
from io import BytesIO


recognizer = sr.Recognizer()


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