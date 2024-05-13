import TableExtractor

def get_merged_value(pdf_path, page):
    def remove_empty(lst):
        removed_result = []
        for i in lst:
            if i['cell'].text != "":
                removed_result.append(i)
        return removed_result

    results = TableExtractor.extract_merged_result(pdf_path, page)
    table = {}
    for i in range(len(results)):
        table[i+1] = remove_empty(results[i])
    return table

if __name__ == "__main__":
    pdf_path = "/home/domni/tasks/py_pdf_stm/pdf/RFI_ZEV-BATTERY.pdf"
    page = 4
    result = get_merged_value(pdf_path, page)
    print(result)
    """
    print("--"*50)
    for i in range(len(result)):
        print(result[i])
        print("-"*100)
    """
