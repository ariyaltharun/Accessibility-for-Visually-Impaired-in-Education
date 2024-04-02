import pyaudio
import logging
import os
import wave
import speech_recognition as sr
from dotenv import load_dotenv
import streamlit as st

from .Summarize import summarize
from utils import store, load, speak, listen


load_dotenv()


def record_lectures(file_name: str) -> None:
    print("Function needs to be implemented")
    logging.info("Started Recording lecture")
    
    # Shamelessly copied from stackoverflow, src: https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = file_name

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK)

    try:
        logging.info("Recording")
        frames = []
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
        logging.info("Recording stopped")

    # Save the wav file in RecordedLectures
    with wave.open("RecordedLectures/"+WAVE_OUTPUT_FILENAME, 'wb') as file:
        file.setnchannels(CHANNELS)
        file.setframerate(RATE)
        file.setsampwidth(p.get_sample_size(FORMAT))
        file.writeframes(b''.join(frames))    
        logging.info("Recording saved")

    text = convertAudioToText(WAVE_OUTPUT_FILENAME)
    summarized_text = summarize(text)
    data = {
        'file_name': WAVE_OUTPUT_FILENAME[:-4],
        'text': text,
        'summerized_text': summarized_text,
        'audio_file': f"audiofiles/{WAVE_OUTPUT_FILENAME}"
    }

    # Store the data in mongodb
    store(os.getenv('MONGO_URL'), "recordings", data)


def convertAudioToText(recorded_audio: str):
    # Convert the same wav file into text (Audio file to text)
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(f"RecordedLectures/{recorded_audio}")

    with audio_file as source:
        audio_text = recognizer.record(source)

    with open(f"recognizedSpeech/{recorded_audio[:-4]}_text.txt", "w") as file:
        text = recognizer.recognize_google(audio_text)
        file.write(text)

    return text


def replay_lecture(wave_file_name: str) -> None:
    # data = {'file_name': wave_file_name}        
    # req_data: dict | None = load(os.getenv('MONGO_URL'), "recordings", data)

    # req_data = "./recognizedSpeech/"+wave_file_name.replace(" ", "_")+".txt"
    req_data = "./recognizedSpeech/new_file.txt"
    if not req_data:
        speak("Lecture not found")
        return
    
    file_contents: str = open(req_data, 'r')
    file_contents = file_contents.read()
    with st.chat_message("assistant"):
        st.write(f"file contents are:\n{file_contents}")
        speak(file_contents)
    # speak("Would you prefer listening to full lecture or summarized lecture?")
    # user_choice: str = listen()
    # if "full lecture" in user_choice:
    #     speak(req_data['text'])
    # elif "summarized lecture" in user_choice:
    #     speak(req_data['summarized_text'])
    
    # return


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET)
    record_lectures("output.wav")
