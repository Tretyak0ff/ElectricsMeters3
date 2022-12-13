from datetime import datetime
from loguru import logger
from tabulate import tabulate
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from pymodbus.client import ModbusTcpClient

from .log.logger import line_1, line_2, line_2_reset
from .tables import Base, TName, TLocation, TModel, TTypeConnection, THost, TPort, TElectricMeter, TIndications, TPeriods
from .models import ElectricMeter
from .settings import Session
from .transport import get_connect, get_verification, get_data_release, get_energy


def get_field_id(table: Base, filter_value: str, session: sessionmaker) -> id:
    field_id = None
    if session.query(table).filter(text('name= :value')).params(value=filter_value).first() is not None:
        for field in session.query(table).filter(text('name=:value')).params(value=filter_value):
            field_id = field.id
    else:
        line = table(
            name=filter_value,
            created=datetime.now(),
            changed=datetime.now()
        )
        session.add(line)
        session.commit()
        session.close()
        for field in session.query(table).filter(text('name=:value')).params(value=filter_value):
            field_id = field.id
    return field_id


def write_electricmeter(electric_meter: ElectricMeter, index: int) -> int:
    electricmeter = {}
    session = Session()

    electricmeter['location.id'] = get_field_id(table=TLocation, filter_value=str(electric_meter.location),
                                                session=session)
    electricmeter['model.id'] = get_field_id(
        table=TModel, filter_value=electric_meter.model, session=session)
    electricmeter['name.id'] = get_field_id(
        table=TName, filter_value=electric_meter.name, session=session)
    if electric_meter.typeconnection is not None:
        electricmeter['typeconnection.id'] = get_field_id(table=TTypeConnection,
                                                          filter_value=electric_meter.typeconnection,
                                                          session=session)
    else:
        electricmeter['typeconnection.id'] = None

    if electric_meter.host is not None:
        electricmeter['host.id'] = get_field_id(
            table=THost, filter_value=electric_meter.host, session=session)
    else:
        electricmeter['host.id'] = None

    if electric_meter.port is not None:
        electricmeter['port.id'] = get_field_id(
            table=TPort, filter_value=str(electric_meter.port), session=session)
    else:
        electricmeter['port.id'] = None

    if electricmeter['host.id'] and electricmeter['port.id'] is not None:
        electricmeter['polling'] = True
    else:
        electricmeter['polling'] = False

    query = session.query(TElectricMeter).filter_by(
        location_id=electricmeter['location.id'],
        model_id=electricmeter['model.id'],
        name_id=electricmeter['name.id'],
        typeconnection_id=electricmeter['typeconnection.id'],
        host_id=electricmeter['host.id'],
        port_id=electricmeter['port.id'],
        serial=electric_meter.serial,
        address=electric_meter.address,
        coefficient=electric_meter.coefficient
    )

    if query.first() is None:
        line = TElectricMeter(
            location_id=electricmeter['location.id'],
            model_id=electricmeter['model.id'],
            name_id=electricmeter['name.id'],
            typeconnection_id=electricmeter['typeconnection.id'],
            host_id=electricmeter['host.id'],
            port_id=electricmeter['port.id'],
            serial=electric_meter.serial,
            address=electric_meter.address,
            polling=electricmeter['polling'],
            coefficient=electric_meter.coefficient,
            generation=False,
            created=datetime.now(),
            changed=datetime.now()
        )
        logger.debug(line)
        # session.add(line)
        # session.commit()
        # session.close()
        index += 1

        electricmeter.clear()
    return index


def read_electricmeters() -> list:
    session = Session()
    electric_meters = session.query(TElectricMeter, TModel, THost, TPort, TLocation, TName). \
        filter(
        TElectricMeter.model_id == TModel.id,
        TElectricMeter.name_id == TName.id,
        TElectricMeter.location_id == TLocation.id,
        TElectricMeter.host_id == THost.id,
        TElectricMeter.port_id == TPort.id,
    ).filter(TElectricMeter.polling == 'True').all()
    return electric_meters


def get_energy_mercury(electric_meter, model_reset: tuple) -> dict:
    global log_line2
    indications = {'connect': get_connect(
        electric_meter=electric_meter, command='open channel')}
    if not indications['connect']:
        logger.error(
            f'\n !!! {electric_meter.THost.name}: {electric_meter.TPort.name} - Error connect!!!')
    if indications['connect']:
        indications['connect'] = get_connect(
            electric_meter=electric_meter, command='serial number')
        indications['verification'] = get_verification(
            electric_meter=electric_meter)
        if not indications['verification']:
            logger.error(f'\n !!! {electric_meter.THost.name}: {electric_meter.TPort.name}/'
                         f'{electric_meter.TElectricMeter.address} - Error verification!!!')
        if indications['verification']:
            logger.debug(
                f'\n >>> {electric_meter.THost.name}: {electric_meter.TPort.name} - Reading socket...')
            indications['data_release'] = get_data_release(
                electric_meter=electric_meter)
            logger.debug(
                f'\n >>> Reading address - {electric_meter.TElectricMeter.address}...')
            # Обработка model_reset
            if electric_meter.TModel.name in model_reset:
                active_plus, active_minus, reactive_plus, reactive_minus = get_energy(
                    electric_meter=electric_meter, command='energy reset')

                reset = {'active_plus': active_plus, 'active_minus': active_minus,
                         'reactive_plus': reactive_plus, 'reactive_minus': reactive_minus}
                indications['energy'] = {'reset': reset, }
                log_line2 = tabulate(line_2_reset(indications=indications),
                                     numalign='right', headers='firstrow', tablefmt="plain")
            else:
                active_plus, active_minus, reactive_plus, reactive_minus = get_energy(
                    electric_meter=electric_meter, command='energy year')
                year = {'active_plus': active_plus, 'active_minus': active_minus,
                        'reactive_plus': reactive_plus, 'reactive_minus': reactive_minus}

                active_plus, active_minus, reactive_plus, reactive_minus = get_energy(
                    electric_meter=electric_meter, command='energy month')
                month = {'active_plus': active_plus, 'active_minus': active_minus,
                         'reactive_plus': reactive_plus, 'reactive_minus': reactive_minus}

                active_plus, active_minus, reactive_plus, reactive_minus = get_energy(
                    electric_meter=electric_meter, command='energy day')
                day = {'active_plus': active_plus, 'active_minus': active_minus,
                       'reactive_plus': reactive_plus, 'reactive_minus': reactive_minus}
                indications['energy'] = {
                    'year': year, 'month': month, 'day': day}
                log_line2 = tabulate(line_2(indications=indications),
                                     numalign='right', headers='firstrow', tablefmt="plain")
        log_line1 = tabulate([line_1(electric_meter=electric_meter)],
                             numalign='right', headers='keys', tablefmt="plain")
        logger.debug(f'\n <<< Unpack and write read data to DB...')
        logger.debug(f'\n{log_line1}')
        logger.debug(f'\n{log_line2}')
    return indications


def get_energy_modbus(electric_meter) -> dict:
    client = ModbusTcpClient(electric_meter.THost.name,
                             electric_meter.TPort.name)
    client.connect()
    try:
        received_data = client.read_holding_registers(
            electric_meter.TElectricMeter.serial, 2, unit=0)
        # assert (received_data.function_code < 0x80)  # test that we are not an error
        energy = bytearray()
        energy.append(received_data.registers[1].to_bytes(2, 'big')[0])
        energy.append(received_data.registers[1].to_bytes(2, 'big')[1])
        energy.append(received_data.registers[0].to_bytes(2, 'big')[0])
        energy.append(received_data.registers[0].to_bytes(2, 'big')[1])
        reset = {'active_plus': int.from_bytes(energy, "big"),
                 'active_minus': 0,
                 'reactive_plus': 0,
                 'reactive_minus': 0}
        indications = {'connect': True, 'verification': True,
                       'energy': {'reset': reset}, }
    except:
        indications = {'connect': False, 'energy': None, }
    return indications


def get_indications(electric_meter, model_modbus: tuple, model_reset: tuple) -> dict:
    if electric_meter.TModel.name in model_modbus:
        indications = get_energy_modbus(electric_meter=electric_meter)
    else:
        indications = get_energy_mercury(
            electric_meter=electric_meter, model_reset=model_reset)
    return indications


def write_indications(electric_meter,  model_modbus: tuple, model_reset: tuple,
                      indications: dict, index: int) -> int:
    session = Session()
    if indications['connect']:
        if indications['verification']:
            index += 1
            if electric_meter.TModel.name in (model_reset or model_modbus):
                line = TIndications(
                    electricmeter_id=electric_meter.TElectricMeter.id,
                    period_id=get_field_id(
                        table=TPeriods, filter_value=str('reset'), session=session),
                    active_plus=indications['energy']['reset']['active_plus'],
                    active_minus=indications['energy']['reset']['active_minus'],
                    reactive_plus=indications['energy']['reset']['reactive_plus'],
                    reactive_minus=indications['energy']['reset']['reactive_minus'],

                    created=datetime.now(),
                    changed=datetime.now()
                )
                session.add(line)
                session.commit()
                session.close()
            else:
                for key in indications['energy'].keys():
                    line = TIndications(
                        electricmeter_id=electric_meter.TElectricMeter.id,
                        period_id=get_field_id(
                            table=TPeriods, filter_value=str(key), session=session),
                        active_plus=indications['energy'][key]['active_plus'],
                        active_minus=indications['energy'][key]['active_minus'],
                        reactive_plus=indications['energy'][key]['reactive_plus'],
                        reactive_minus=indications['energy'][key]['reactive_minus'],

                        created=datetime.now(),
                        changed=datetime.now(),
                    )
                    session.add(line)
                    session.commit()
                    session.close()
    return index
