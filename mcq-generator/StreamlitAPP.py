
import os
import sys
import json
import pandas as pd
import streamlit as st
import traceback

# This is a crucial step to ensure Streamlit can find the mcqgenerator module
# It adds the 'src' directory to Python's path
from src.mcqgenerator.utils import read_file, get_table_data, extract_quiz_data
from src.mcqgenerator.MCQGenerator import final_chain
from src.mcqgenerator.logger import logging

try:
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the 'src' directory
    src_path = os.path.join(current_dir, 'src')
    # Add the 'src' directory to the system path
    if src_path not in sys.path:
        sys.path.append(src_path)

    from mcqgenerator.utils import read_file, get_table_data, extract_quiz_data
    from mcqgenerator.MCQGenerator import final_chain
    from mcqgenerator.logger import logging

except ImportError as e:
    # If imports fail, show a helpful error message in the Streamlit app
    st.error(
        f"Failed to import necessary modules: {e}\n"
        "Please ensure the file structure is correct: \n"
        "- Your Streamlit app should be in `mcq-generator/StreamlitAPP.py`\n"
        "- Your modules should be in `mcq-generator/src/mcqgenerator/`"
    )
    st.stop() # Stop the app if modules can't be loaded


# --- App UI Configuration ---
st.set_page_config(
    page_title="MCQ Generator | Gemini & LangChain",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Main Application ---
st.title("🤖 AI-Powered MCQ Generator")
st.markdown("""
Welcome! This application uses Google's Gemini Pro model via LangChain to generate Multiple Choice Quizzes from your uploaded documents.

**How to use:**
1.  Upload a document (`.pdf` or `.txt`).
2.  Specify the number of questions you want.
3.  Enter the subject of the quiz.
4.  Choose the desired difficulty level.
5.  Click "Create MCQs" and see the magic happen!
""")

# --- Input Form ---
with st.form("user_inputs_form"):
    st.header("Quiz Configuration")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your document (PDF or TXT)", type=["pdf", "txt"])
    
    # Number of questions (MCQ Count)
    mcq_count = st.number_input("Number of Questions", min_value=3, max_value=15, value=5)
    
    # Subject/Topic
    subject = st.text_input("Enter the Subject", max_chars=60, placeholder="e.g., Python Programming")
    
    # Tone/Difficulty
    tone = st.selectbox("Select Quiz Difficulty", ("Simple", "Medium", "Hard"))
    
    # Submit Button
    submit_button = st.form_submit_button(label="✨ Create MCQs")

# --- Processing Logic ---
if submit_button:
    # Validate inputs
    if not all([uploaded_file, subject, mcq_count, tone]):
        st.warning("Please fill out all the fields before submitting.")
    else:
        with st.spinner("Generating your quiz... This might take a few moments."):
            try:
                # Read the text content from the uploaded file
                text = read_file(uploaded_file)
                
                # Define the JSON structure placeholder for the prompt
                response_json_placeholder = {
                    str(i): {
                        "mcq": "multiple choice question",
                        "options": {
                            "a": "choice here", "b": "choice here",
                            "c": "choice here", "d": "choice here"
                        },
                        "correct": "correct answer",
                    } for i in range(1, mcq_count + 1)
                }
                
                # Get the LangChain chain for generation and evaluation
                
                
                # Invoke the chain with all the necessary inputs
                response = final_chain.invoke({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(response_json_placeholder)
                })
                
                # Check if the response and the quiz part of it are valid
                if response and "quiz" in response:
                    quiz_string = response["quiz"]
                    
                    # Robustly extract JSON from the potentially messy model output
                    quiz_data = extract_quiz_data(quiz_string)
                    
                    if quiz_data:
                        # Format the parsed data for table display
                        quiz_table_data = get_table_data(quiz_data)
                        
                        if quiz_table_data:
                            df = pd.DataFrame(quiz_table_data)
                            df.index = df.index + 1 # Start index from 1
                            
                            # Store results in session state to persist them
                            st.session_state.quiz_df = df
                            st.session_state.review = response.get("review", "")
                            
                            st.success("Your quiz has been generated successfully!")
                        else:
                            st.error("Failed to format the generated quiz data.")
                    else:
                        st.error("The model returned a response, but it couldn't be parsed as valid JSON. Please try again.")
                        logging.error("JSON Parsing Error from model output: %s", quiz_string)
                else:
                    st.error("The model failed to generate a response. Please check your API key and try again.")
            
            except Exception as e:
                logging.error(traceback.format_exc())
                st.error(f"An unexpected error occurred: {e}")

# --- Display Results ---
# Check if a quiz dataframe is stored in the session and display it
if "quiz_df" in st.session_state and isinstance(st.session_state.quiz_df, pd.DataFrame):
    st.subheader("📝 Generated Multiple Choice Quiz")
    st.dataframe(st.session_state.quiz_df)
    
    # Display the review if it exists
    if st.session_state.get("review"):
        st.subheader("🧐 AI-Generated Review")
        st.write(st.session_state.review)
        
    # Add a button to clear the output
    if st.button("Clear and Start Over"):
        # Clear the session state and rerun the app
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()