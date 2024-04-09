import PyPDF2
import logging
from utils import listen, speak
from time import sleep
import streamlit as st
import base64

# gif from local file
file_ = open("listen.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

# Make a get request to download pdf question paper 
# or get qp when teacher uploads qp to website
# For simmulation, using sample.pdf file 
def getQP():
    # This functions just downloads and save in certain directory
    # Nothing inside
    pass


def parsePDFToQuestions(path_to_pdf: str) -> list[str]:
    # Challenge is parsing pdf and converting to list of correct question 
    # (meaning list element should not contain truncated questions) 
    """Parses PDF to list of questions
    Args:
    ----
    path_to_pdf (str)

    Output:
    ------
    returns list of questions
    """
    logging.info("Parsing PDF file to list of questions")
    with open(path_to_pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        content = list()
        for page in reader.pages:
            content.append(page.extract_text())

    qp_text = ' '.join(content)

    # Check for simple case (Heuristics)
    # Consider every line as one question (Later use regular exp to extract only questions)
    logging.info(qp_text.split("\n"))
    questions = qp_text.split("\n")
    return questions


def convertQuestionsToDict(questions: list[str]) -> list[dict]:
    """Converts each question in the list to list of dict
    dict format
    ```python
    question_answer_list[i] = {
        'Question': questions[i],
        'Answer': None, 
        'Voice_file': None
    }
    ```
    i -> ith question in questions

    Args:
    -----
    questions: List of questions

    Output:
    -------
    question_answer_list
    """
    question_answer_list = list()
    for question in questions:
        question_answer_dict = {
            'Question': question,
            'Answer': None,
            'Voice_File': None
        }
        question_answer_list.append(question_answer_dict)
    return question_answer_list


# Function name doesn't sound good, please change
def fillAnswers(question_answer_list: list[dict]) -> list[dict]:
    question_no = 0
    while question_no != len(question_answer_list):
        # Say the question to user
        logging.info("Dictating the question")
        with st.chat_message("assistant"):
            speak(question_answer_list[question_no]['Question'])
            st.write(question_answer_list[question_no]['Question'])
            # Sleep for few seconds
            sleep(0.5)
            # Ask whether user to repeat the question or wants to answer
            logging.info("Asking if question must be repeated.")
            st.write("Do you want the question to be repeated?")
            speak("Do you want the question to be repeated?")

        # Start recording and convert to text
        visualize_listening_container = st.empty()
        listening_text_container = st.empty()
        visualize_listening_container.markdown(
            f'<img src="data:image/gif;base64,{data_url}" width=200 alt="listening gif">',
            unsafe_allow_html=True,
        )
        listening_text_container.write("Listening...")
        user_answer: str = listen()
        visualize_listening_container.empty()
        listening_text_container.empty()  

        with st.chat_message("user"):
            st.write(user_answer)
            
        if "Yes" in user_answer:
            speak("Repeating the question again, listen carefully")
            # Maybe sleep for few seconds 
            sleep(0.5)
            continue

        speak("Please tell your answer")
        # Start recording the answer for the question and convert to text
        visualize_listening_container = st.empty()
        listening_text_container = st.empty()
        visualize_listening_container.markdown(
            f'<img src="data:image/gif;base64,{data_url}" width=200 alt="listening gif">',
            unsafe_allow_html=True,
        )
        listening_text_container.write("Listening...")
        user_answer: str = listen()
        visualize_listening_container.empty()
        listening_text_container.empty()  

        # confirm whether user satisfied with answer
        logging.info("Asking user whether satisfied or repeat the answer")
        speak("Are you satisfied with answer or do you want to repeat the answer")
        visualize_listening_container = st.empty()
        listening_text_container = st.empty()
        visualize_listening_container.markdown(
            f'<img src="data:image/gif;base64,{data_url}" width=200 alt="listening gif">',
            unsafe_allow_html=True,
        )
        listening_text_container.write("Listening...")
        user_confirmation: str = listen()
        visualize_listening_container.empty()
        listening_text_container.empty()  

        if "satisfied" in user_confirmation:
            logging.info("User confirmed")
            question_answer_list[question_no]['Answer'] = user_answer
            question_answer_list[question_no]['Voice_File'] = None # Optional
            question_no += 1
            speak("Continuing with next question")
            # Maybe Sleep for 0.5 seconds
            sleep(0.5)
            continue

        if "repeat answer" in user_confirmation:
            speak(question_answer_list[question_no]['Answer'])
            # Maybe Sleep for 0.5 seconds
            sleep(0.5)
            speak("Do you want change the answer?")

            visualize_listening_container = st.empty()
            listening_text_container = st.empty()
            visualize_listening_container.markdown(
                f'<img src="data:image/gif;base64,{data_url}" width=200 alt="listening gif">',
                unsafe_allow_html=True,
            )
            listening_text_container.write("Listening...")
            user_confirmation: str = listen()
            visualize_listening_container.empty()
            listening_text_container.empty()  

            if "yes" in user_confirmation:
                speak("Please listen the question again and answer correctly")
                continue
            
            if "no" in user_confirmation:
                speak(f"You answered question {question_no}")
                question_answer_list[question_no]['Answer'] = user_answer
                question_answer_list[question_no]['Voice_File'] = None # Optional
                question_no += 1
                speak("Continuing with next question")
                # Maybe Sleep for 0.5 seconds
                sleep(0.5) 
                continue

    logging.info(question_answer_list)
    return question_answer_list


def saveAnswersToTxtFile(question_answer_list: list[dict], file_name: str="Exam/answers.txt") -> None:
    with open(file_name, "w") as file:
        for e, data in enumerate(question_answer_list):
            file.writelines(f"{e+1}) {data['Question']}\nAnswer: {data['Answer']}\n\n")
    return


def scribe() -> None:
    # Add a function to download qp
    questions_list = parsePDFToQuestions("Exam/sample.pdf")
    # sleep for few seconds
    speak("Exam starting now")
    sleep(0.5)    
    speak("Answer the questions carefully")
    sleep(0.5)
    question_answer_list = convertQuestionsToDict(questions_list)
    answered_ds = fillAnswers(question_answer_list)
    saveAnswersToTxtFile(answered_ds)
    return


if __name__ == "__main__":
    scribe()
