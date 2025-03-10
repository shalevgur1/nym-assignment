import pdfplumber
from nym_assignment.assignment_api import NymAssignmentApi


PDF_PATH_Example = "./chart_example.pdf"
PDF_PATH_1 = "./chart1.pdf"
PDF_PATH_2 = "./chart1.pdf"
PDF_PATH_3 = "./chart1.pdf"



def main():
    api_instance = NymAssignmentApi()
    result = api_instance.pdf_to_dict(PDF_PATH_Example)
    print(result)




if __name__ == "__main__":
    main()