import logging
from datetime import datetime

from loguru import logger
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from .models import ElectricMeter
from .tables import Base, TName, TLocation, TModel, TTypeConnection, THost, TPort, TElectricMeter, \
    TPropertys, TOptions, TPeriods, TIndications
from .settings import Session


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
    electricmeter['model.id'] = get_field_id(table=TModel, filter_value=electric_meter.model, session=session)
    electricmeter['name.id'] = get_field_id(table=TName, filter_value=electric_meter.name, session=session)
    if electric_meter.typeconnection is not None:
        electricmeter['typeconnection.id'] = get_field_id(table=TTypeConnection,
                                                          filter_value=electric_meter.typeconnection,
                                                          session=session)
    else:
        electricmeter['typeconnection.id'] = None

    if electric_meter.host is not None:
        electricmeter['host.id'] = get_field_id(table=THost, filter_value=electric_meter.host, session=session)
    else:
        electricmeter['host.id'] = None

    if electric_meter.port is not None:
        electricmeter['port.id'] = get_field_id(table=TPort, filter_value=str(electric_meter.port), session=session)
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
        session.add(line)
        session.commit()
        session.close()
        index += 1

        electricmeter.clear()
    return index


def read_electricmeter() -> list:
    session = Session()

    electric_meters = session.query(TElectricMeter, TModel, THost, TPort, TLocation, TName).\
        filter(
        TElectricMeter.model_id == TModel.id,
        TElectricMeter.name_id == TName.id,
        TElectricMeter.location_id == TLocation.id,
        TElectricMeter.host_id == THost.id,
        TElectricMeter.port_id == TPort.id,
    ).filter(TElectricMeter.polling == 'True').all()
    return electric_meters
