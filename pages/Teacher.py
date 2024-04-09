import streamlit as st

st.title("Teachers Portal to Upload the Question Papers")
with st.form("File upload"):
    subject_name = st.text_input("Subject", "")
    class_number = st.number_input("Class", step=1)
    st.file_uploader("Upload the question paper")
    file_upload_submit_btn = st.form_submit_button()
