import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from utils.file import read_excel
from utils.database import write_electricmeter, read_electricmeters, get_indications, write_indications


load_dotenv(find_dotenv())

logger.add('utils/log/.log', format='{time:DD/MM/YYYY HH:mm:ss}{message}',
           level='INFO',
           rotation='1 week',
           compression='zip')


def get_number() -> int:
    while type:
        entered_text = input(f'Select item: \n'
                             f'1. Filling the database from excel file \n'
                             f'2. Interrogation of electricmeters \n')
        try:
            entered_number = int(entered_text)
        except ValueError:
            print(f'{entered_text} - is not a number')
        else:
            break
    return abs(entered_number)



def filling():
    if not os.path.isfile(f"local/{ os.environ.get('NAME_EXCEL_FILE') }"):

        print(f'Place file "ListElectricMeter.xlsx" to the local folder')
    else:
        electrics_meters = read_excel(
            excel_file=f"local/{ os.environ.get('NAME_EXCEL_FILE') }", read_only=True)
        num_reads = 0
        num_records = 0
        for electric_meter in electrics_meters:
            logger.debug(electric_meter)
            num_reads += 1
            num_records = write_electricmeter(
                electric_meter=electric_meter, index=num_records)
        logger.debug(
            f'Read from file {num_reads} line(s), added to DB {num_records} line(s)')


def pulling():
    num_goods = 0
    model_modbus = ('Панель PCC33MLD',)
    model_reset = ('Меркурий-230 AR-00 R',)

    logger.info(f'\n *** Request data from electric meters...'
                f'\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    electric_meters = read_electricmeters()
    num_reads = len(electric_meters)
    for electric_meter in electric_meters:
        # logger.warning(electric_meter.TModel.name)
        indications = get_indications(electric_meter=electric_meter,
                                      model_modbus=model_modbus, model_reset=model_reset, )
        num_goods = write_indications(electric_meter=electric_meter,
                                      model_modbus=model_modbus, model_reset=model_reset,
                                      indications=indications, index=num_goods)
    logger.info(f'\n *** Data read from {num_goods} of {num_reads} electric meter(s)'
                f'\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def main():
    number = get_number()
    logger.debug(('select number', number))
    match number:
        case 1:
            filling()
        case 2:
            pulling()
        case _:
            logger.debug(('пока не придумал', number))


if __name__ == '__main__':
    main()
