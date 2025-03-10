import pdfplumber
from dataclasses import dataclass
from typing import List, Dict 



@dataclass 
class TextualWord: 
    x0: float 
    x1: float 
    text: str 

PagesToWords = Dict[int, List[TextualWord]]

class NymAssignmentApi:
    
    def __init__(self):
        pass

    def pdf_to_dict(self, pdf_path: str) -> PagesToWords:

        current_PagesToWords: PagesToWords = {}

        with pdfplumber.open(pdf_path) as pdf:
            
            for page in pdf.pages:
                current_number = page.page_number
                current_words = page.extract_words()
                for word in current_words:
                    current_textual_word = TextualWord(x0=word['x0'], x1=word['x1'], text=word['text'])
                    if current_number not in current_PagesToWords:
                        current_PagesToWords[current_number] = []
                    current_PagesToWords[current_number].append(current_textual_word)
        
        return current_PagesToWords