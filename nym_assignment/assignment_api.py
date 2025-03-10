import pdfplumber
from dataclasses import dataclass
from typing import List, Dict 
from datetime import date
from datetime import datetime
import re


@dataclass 
class TextualWord: 
    x0: float 
    x1: float 
    text: str 


@dataclass 
class Chart: 
    name: str 
    dob: date 
    has_valid_ekg: bool 

    @property 
    def age(self) -> float: 
        current_time = date.today()
        age = current_time.year - self.dob.year
        if current_time.month < self.dob.month or (current_time.month == self.dob.month and current_time.day < self.dob.day):
            # Didn't have birthday this year yet
            age -= 1
        return age
    
    def to_string(self) -> str:
        return f"Name: {self.name}\nDate of Birth: {self.dob}\nAge: {self.age}\nValid EKG: {self.has_valid_ekg}"


PagesToWords = Dict[int, List[TextualWord]]

class NymAssignmentApi:
    
    def __init__(self):
        pass

    def pdf_to_dict(self, pdf_path: str) -> PagesToWords:
        # Uses the pdfplumber tool to extract pdf text and divide it to words
        # for every page (as requested in the question). Uses the extract_words() method
        # for the page object from the pdfplumber tool.
        # Use pdf path as input to extract the text from the pdf.

        current_PagesToWords: PagesToWords = {}

        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from pdf using given path

            for page in pdf.pages:
                # Iterate over the pages
                current_number = page.page_number
                current_words = page.extract_words()
                for word in current_words:
                    # Iterate over words
                    current_textual_word = TextualWord(x0=word['x0'], x1=word['x1'], text=word['text'])
                    if current_number not in current_PagesToWords:
                        current_PagesToWords[current_number] = []
                    current_PagesToWords[current_number].append(current_textual_word)
        
        return current_PagesToWords
    
    def populate_chart(self, page_to_words: PagesToWords) -> Chart:
        # Iterate over all the words in the page_to_words from the pdf.
        # Set anchors according to the pdfs general strucures dynamiclly according to 
        # given pdf to identify fields.
        # Examples: 
        # 1. Set start of line to the position of the first word (x0) - dynamic.
        # 2. Search for defined words like 'Name:' 'DOB:' and 'Lab'.
        # 3. Collects all the lines related to the 'Lab' results and use regular expressions
        # on every line to find the validity of the EKG. Stops search for Lab results lines
        # when incounter 'Radiology'.

        newline_anchor = page_to_words[1][0].x0
        input_flag = ''
        lab_input_flag = False
        previous_x0 = 0.0
        lab_text_lines = []
        text_line = ""

        current_name: str = ''
        current_dob: date = None
        current_has_valid_ekg: bool = False

        for page_number in page_to_words:
            for word in page_to_words[page_number]:
                if (word.text == 'Name:' or word.text == "DOB:"):
                    # Find Name or DOB fields that has data on the same line
                    input_flag = word.text
                elif input_flag:
                    # Handle Name and DOB values
                    if word.x0 == newline_anchor:
                        input_flag = ''
                    else:
                        if input_flag == 'Name:':
                            current_name += word.text + ' '
                        elif input_flag == "DOB:":
                            date_str = word.text
                            current_dob = datetime.strptime(date_str, '%m/%d/%Y').date()
                elif word.text == "Lab":
                    # Find Lab field that has multiline data
                    lab_input_flag = True
                    previous_x0 = word.x0
                elif lab_input_flag:
                    # Start collecting text lines
                    if previous_x0 > word.x0:
                        # New line in pdf
                        if word.text == "Radiology":
                            lab_input_flag = False
                        if text_line:
                            lab_text_lines.append(text_line)
                            text_line = ""
                    text_line += word.text + " "
                    previous_x0 = word.x0

        # Search for EKG field in lab results different lines.
        # If the line with the EKG field includes a negative word (no/not) - EKG is not valid
        pattern_ekg = r'\bEKG\b'
        pattern_no_not = r'\b(?:no|not)\b'
        for line in lab_text_lines:
            if re.search(pattern_ekg, line, re.IGNORECASE):
                # Found 'ekg' in line
                if not re.search(pattern_no_not, line, re.IGNORECASE):
                    # Can't find 'no' or 'not' in line - ekg is valid
                    current_has_valid_ekg = True

        # Create chart instance
        current_chart = Chart(name=current_name, dob=current_dob, has_valid_ekg=current_has_valid_ekg)

        return current_chart