import streamlit as st
import pymongo
import pdfplumber
import re

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://test:test@cluster0.lnvvyxl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["pdf_database"]
collection = db["pdf_collection"]

# Function to extract questions from PDF and store them in MongoDB
def extract_questions_and_store(pdf_file, subject, class_name):
    with pdfplumber.open(pdf_file) as pdf:
        questions = []
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            potential_question = ""
            for line in lines:
                line = line.strip()
                if re.match(r'^[0-9]+\.', line):  # Start of a new potential question
                    if potential_question:  # If not the first question, store the previous one
                        questions.append(potential_question.strip())
                    potential_question = line  # Start a new potential question
                else:
                    potential_question += " " + line  # Add line to potential question
            
            if potential_question:  # Add the last potential question
                questions.append(potential_question.strip())
    
    # Filter out non-question sentences
    questions = [question for question in questions if re.match(r'^[0-9]+\.', question)]
    
    # Store questions, subject, and class in MongoDB
    document = {
        "questions": questions,
        "subject": subject,
        "class": class_name
    }
    collection.insert_one(document)
    return questions

# Streamlit UI
def main():
    st.title("PDF Question Extractor and MongoDB Storer")
    subject = st.text_input("Enter the subject:")
    class_name = st.text_input("Enter the class:")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Submit"):
            questions = extract_questions_and_store(uploaded_file, subject, class_name)
            st.success("Questions extracted and stored successfully in MongoDB!")
            st.write("Extracted Questions:")
            for question in questions:
                st.write(question)

if __name__ == "__main__":
    main()
