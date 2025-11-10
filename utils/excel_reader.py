import openpyxl


def read_excel_data(file_path, sheetName):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheetName]

    # Clean header names
    headers = []
    for cell in sheet[1]:
        if cell.value is not None:
            clean_header = str(cell.value).strip().replace(" ", "_")
            headers.append(clean_header)
        else:
            headers.append("Unnamed")

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Combine header names with row values
        row_dict = dict(zip(headers, row))
        data.append(row_dict)

    return data
