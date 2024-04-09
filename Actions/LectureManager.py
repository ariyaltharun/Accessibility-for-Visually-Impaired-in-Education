import pyaudio
import logging
import keyboard
import os
import wave
import base64
import speech_recognition as sr
from dotenv import load_dotenv
import streamlit as st
import requests
import json

from .Summarize import summarize
from utils import store, load, speak, listen


load_dotenv()

# gif from local file
file_ = open("listen.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


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
            if keyboard.is_pressed('q'):
                raise Exception
    except Exception:
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
    

    ############################# Text Enhancement ################################
    URL = "<PASTE-URL-GENERATED-IN-COLAB>/text_enhance"
    data = {
        "text": text,
        "summary_text": summarized_text,
        "lan": "en",
        "len_limit": 1000
    }
    response = requests.post(
        URL,
        json=data
    )
    if response.ok:
        data = json.loads(response.content)
        text = data["text"]
        summarized_text = data["summary_text"]
    ##############################################################################

    data = {
        'file_name': WAVE_OUTPUT_FILENAME[:-4],
        'text': text,
        'summarized_text': summarized_text,
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
    data = {'file_name': wave_file_name}        
    req_data: dict | None = load(os.getenv('MONGO_URL'), "recordings", data)
    print(req_data)

    # req_data = "./recognizedSpeech/"+wave_file_name.replace(" ", "_")+"_text.txt"
    # req_data = "./recognizedSpeech/new_file.txt"
    if not req_data:
        speak("Lecture not found")
        return
    
    # file_contents: str = open(req_data, 'r')
    # file_contents = file_contents.read()
    with st.chat_message("assistant"):
        # st.write(f"file contents are:\n{file_contents}")
        # speak(file_contents)
        st.write("Would you prefer listening to full lecture or summarized lecture?")
        speak("Would you prefer listening to full lecture or summarized lecture?")
    
    with st.chat_message("user"):
        visualize_listening_container = st.empty()
        listening_text_container = st.empty()
        visualize_listening_container.markdown(
            f'<img src="data:image/gif;base64,{data_url}" width=200 alt="listening gif">',
            unsafe_allow_html=True,
        )
        listening_text_container.write("Listening...")
        user_choice: str = listen()
        visualize_listening_container.empty()
        listening_text_container.empty()  

        st.write(user_choice)

    with st.chat_message("assistant"):
        if "full lecture" in user_choice:
            st.write(req_data['text'])
            speak(req_data['text'])
        elif "summarized lecture" in user_choice:
            st.write(req_data['summarized_text'])
            speak(req_data['summarized_text'])
    
    # return


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET)
    record_lectures("output.wav")
