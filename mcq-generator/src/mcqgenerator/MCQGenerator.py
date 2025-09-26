import os
import json
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# --- Setup ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# --- Prompt Templates ---
TEMPLATE = '''
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to 
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. 
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
'''

TEMPLATE2 = '''
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
'''

# --- Prompt Definitions ---
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"], 
    template=TEMPLATE2
)

# --- MODERN LCEL CHAIN DEFINITION (This is the correct part) ---

# 1. Define the first chain: Quiz Generation
quiz_chain = quiz_generation_prompt | llm | StrOutputParser()

# 2. Define the second chain: Quiz Review
review_chain = quiz_evaluation_prompt | llm | StrOutputParser()

# 3. Combine them into a final sequential chain using LCEL
final_chain = RunnablePassthrough.assign(quiz=quiz_chain) | {
    "quiz": lambda x: x["quiz"],  # Pass the generated quiz through to the final output
    "review": review_chain       # Run the review chain on the output of the first step
}