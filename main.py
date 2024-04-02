import logging
from time import sleep
import speech_recognition as sr
import streamlit as st
import streamlit.components.v1 as components
import base64

from utils import listen, speak
from Actions.LectureManager import record_lectures, replay_lecture
from Actions.Scribe import scribe


logging.basicConfig(level=logging.NOTSET, format="[ %(levelname)s ] %(message)s")


recognizer = sr.Recognizer()


user_text: str = None
system_text: str = None
button_click: bool = False
exit: bool = False

# def response_generator():


def actions(user_text) -> None:
    global exit
    if not user_text:
        return
    
    if "record lectures" in user_text:
        # TODO: Record Lectures function
        # Start recording the lectures by activating certain devices e.g,. microphone
        # Give a name to the lecture
        # Store in a database

        with st.chat_message("assistant"):
            st.write("Started Recording Lectures!")
            speak("Started Recording Lectures")
            st.write("What would you name this lecture?")
            speak("What would you name this lecture?")

        filename = listen()
        with st.chat_message("user"):
            st.write(filename)
        st.session_state.messages.append({"role": "user", "content": filename})

        with st.chat_message("assistant"):
            st.markdown(f"{filename} name is cool")
        speak(f"{filename} name is cool")
        filename = filename.replace(" ", "_") + ".wav"
        record_lectures(filename)
        pass
    elif "replay lectures" in user_text:
        # TODO: replay Lectures function
        # Search a lecture based on user_query(name of lecture) in the database
        # Play the lecture
        with st.chat_message("assistant"):
            st.write("Started Replaying Lectures.")
            speak("Started Replaying Lectures")
            sleep(0.5)
            st.write("Which lecture do you want to listen to, again?")
            speak("Which lecture do you want to listen to, again?")

        user_response: str = listen()
        with st.chat_message("user"):
            st.write(user_response)

        replay_lecture(user_response.replace(" ", "_"))
        pass
    elif "scribe" in user_text.lower():
        # TODO: scribe function
        with st.chat_message("assistant"):
            speak("Started Acting as a scribe")
            st.write("Started Acting as a scribe.")
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

    st.title("Education for Visually Impaired")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("5"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write("How can I help you?")
            speak("How can I help you?")
            # gif from local file
            file_ = open("listen.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" width=200 alt="listening gif">',
                unsafe_allow_html=True,
            )
            st.write("Listening...")
            user_text = listen()
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("user"):
            st.markdown(user_text)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_text})

        # with st.chat_message("assistant"):
        system_text = actions(user_text)
        st.write(system_text)
        speak(system_text)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": system_text})

    # button = st.button(label="On Microphone")

    # if button:
        
        
        


if __name__ == "__main__":
    main()


# Reference:
# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps