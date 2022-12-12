import openpyxl
from loguru import logger
from .models import ElectricMeter


def read_excel(excel_file: str, read_only: bool) -> list:
    excel_file = openpyxl.load_workbook(excel_file, read_only=read_only)
    sheet = excel_file.active
    electrics_meters = [
        ElectricMeter(
            name=sheet[row][1].value,
            location=sheet[row][2].value,
            model=sheet[row][3].value,
            serial=sheet[row][4].value,
            typeconnection=sheet[row][5].value,
            host=sheet[row][6].value,
            port=sheet[row][7].value,
            coefficient=sheet[row][8].value,
            comments=sheet[row][9].value
        )
        for row in range(2, sheet.max_row + 1)]
    return electrics_meters
