import pdfplumber
from tabulate import tabulate
import MergeValueExtractor

import os
import json

def get_table_data(pdf_path, page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        tables = page.extract_tables()
        table_data = {}
        if tables:
            for table_number, table in enumerate(tables, start=1):
                table_data[table_number] = [[cell if isinstance(cell, str) else '' for cell in row] for row in table]
    return table_data

def get_table_data1(pdf_path, page):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page]
        tables = page.extract_tables()
        if tables:
            print("\nTables found:")
            for table_number, table in enumerate(tables, start=1):
                    print(f"Table {table_number}:")
                    table_data = [[cell if isinstance(cell, str) else '' for cell in row] for row in table]
                    print(tabulate(table_data, tablefmt="grid"))
                    print("\n")

def copy_merge(result, merge):
    if len(merge['tables'])!=0:
        for table_number in merge['tables']:
            if len(merge['tables'][table_number]) !=0:
                for i in merge['tables'][table_number]:
                    result['tables'][table_number][i['row']][i['column']] = i['cell'].text
        return result
    else:
        return result

def print_table(out):
    print(tabulate(out,tablefmt="grid"))

def extract_text_and_table(pdf_path):
    result = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_content = {}

            table_data = get_table_data(pdf_path, page_number-1)
            #table_data = get_table_data1(page)
            page_content['tables'] = table_data

            merge_content = {}
            merge_content['page'] = page_number
            merge_content['tables'] = MergeValueExtractor.get_merged_value(pdf_path, page_number-1)

            final_result = copy_merge(page_content, merge_content)
            """
            print("page:",page_number)
            for i in final_result['tables']:
                print("table:",i)
                print_table(final_result['tables'][i])
                print("-"*100)
            """

            result[page_number] = copy_merge(page_content, merge_content)
    json_path = "result_pdf/"+os.path.splitext(os.path.basename(pdf_path))[0]+".json"
    with open(json_path, "w") as my_file:
        json.dump(result, my_file)


if __name__ == '__main__':
    pdf_file_path = '/home/domni/tasks/py_pdf_stm/pdf/RFI_ZEV-BATTERY.pdf'
    #pdf_file_path = "/home/domni/tasks/py_pdf_stm/pdf/RFQ1 Summary HV Battery_BMS_RFQ_summary.pdf"
    #pdf_file_path = '/home/domni/tasks/py_pdf_stm/pdf/test_pdf.pdf'
    page_num = 0
    #get_table_data1(pdf_file_path, page_num)
    extract_text_and_table(pdf_file_path)
