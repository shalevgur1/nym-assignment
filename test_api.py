from nym_assignment.assignment_api import NymAssignmentApi


PDF_PATH_Example = "./chart_example.pdf"
PDF_PATH_1 = "./chart1.pdf"
PDF_PATH_2 = "./chart2.pdf"
PDF_PATH_3 = "./chart3.pdf"



def main():
    api_instance = NymAssignmentApi()
    page_to_words = api_instance.pdf_to_dict(PDF_PATH_1)
    chart_instance = api_instance.populate_chart(page_to_words)
    print(chart_instance.to_string())
    page_to_words_extra = api_instance.pdf_to_extra_dict(PDF_PATH_Example)
    for number in page_to_words_extra:
            print(number)
            for word_info in page_to_words_extra[number]:
                print(word_info)




if __name__ == "__main__":
    main()