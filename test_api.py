import pdfplumber
from nym_assignment.assignment_api import NymAssignmentApi


PDF_PATH_Example = "./chart_example.pdf"
PDF_PATH_1 = "./chart1.pdf"
PDF_PATH_2 = "./chart2.pdf"
PDF_PATH_3 = "./chart3.pdf"



def main():
    api_instance = NymAssignmentApi()
    page_to_words = api_instance.pdf_to_dict(PDF_PATH_1)
    result = api_instance.populate_chart(page_to_words)




if __name__ == "__main__":
    main()