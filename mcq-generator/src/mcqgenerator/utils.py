import os
import json
import traceback
from pypdf import PdfReader # CORRECTED: Was 'from PyPDF import PdfReader'

def read_file(file):
    """Reads the content of an uploaded file (PDF or TXT)."""
    if file.name.endswith(".pdf"):
        try:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or "" # Add 'or ""' for safety
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file")
    
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format. Only PDF and TXT files are supported.")

def extract_quiz_data(quiz_string: str) -> dict | None:
    """
    Extracts a JSON object from a string that might be wrapped in markdown.
    Returns the parsed dictionary or None if parsing fails.
    """
    try:
        # Find the first '{' and the last '}' to isolate the JSON object
        start_index = quiz_string.find('{')
        end_index = quiz_string.rfind('}') + 1
        if start_index != -1 and end_index != 0:
            cleaned_json_string = quiz_string[start_index:end_index]
            quiz_data = json.loads(cleaned_json_string)
            return quiz_data
    except (json.JSONDecodeError, IndexError):
        # Fails silently if parsing is not possible, returns None
        pass
    return None

def get_table_data(quiz_data: dict) -> list | bool:
    """
    Formats the parsed quiz dictionary into a list of dicts for table display.
    This function expects a dictionary, not a string.
    """
    try:
        quiz_table_data = []
        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_data.items():
            mcq = value.get("mcq", "")
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value.get("options", {}).items()
                ]
            )
            correct = value.get("correct", "")
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False