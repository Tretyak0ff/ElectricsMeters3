import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from local.utils.settings import Session
from utils import read_excel, write_electricmeter
load_dotenv(find_dotenv())


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
    if not os.path.isfile(os.environ.get('NAME_EXCEL_FILE')):
        print(f'Place file "ListElectricMeter.xlsx" to the local folder')
    else:
        electrics_meters = read_excel(excel_file=os.environ.get('NAME_EXCEL_FILE'), read_only=True)
        num_reads = 0
        num_records = 0
        for electric_meter in electrics_meters:
            logger.debug(electric_meter)
            num_reads += 1
            num_records = write_electricmeter(electric_meter=electric_meter, index=num_records)
        logger.debug(f'Read from file {num_reads} line(s), added to DB {num_records} line(s)')


def pulling():
    num_goods = 0
    session = Session()
    logger.info(f'\n *** Request data from electric meters...'
                f'\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    electric_meters = session.query(
        ElectricMeter, Model, Host, Port, Location, Name
    ).filter(
        ElectricMeter.model_id == Model.id,
        ElectricMeter.name_id == Name.id,
        ElectricMeter.location_id == Location.id,
        ElectricMeter.host_id == Host.id,
        ElectricMeter.port_id == Port.id,
    ).filter(
        ElectricMeter.polling == 'True'
    ).all()
    num_reads = len(electric_meters)



def main():
    number = get_number()
    logger.debug(('select number', number))
    match number:
        case 1:
            filling()
        case 2:
            pulling()
        case _:
            logger.debug(('хуйня какая-то', number))



if __name__ == '__main__':
    main()
