import socket
from datetime import datetime
from local.utils.service import get_ping, get_open_channel, get_close_channel, get_serial_number, \
    get_energy_year, get_energy_month, get_energy_day, get_energy_reset
from local.utils.service import unpack_serial_number, unpack_data_release, unpack_energy


def get_command_mercury(address: int, command: str) -> bytearray:
    """Returns the modbus command"""
    current_month = datetime.now().month
    match command:
        case 'ping':
            command = get_ping(address)
        case 'open channel':
            command = get_open_channel(address)
        case 'close channel':
            command = get_close_channel(address)
        case 'serial number':
            command = get_serial_number(address)
        case 'energy year':
            command = get_energy_year(address)
        case 'energy month':
            command = get_energy_month(address, current_month)
        case 'energy day':
            command = get_energy_day(address)
        case 'energy reset':
            command = get_energy_reset(address)
    return command


def exchange_data(electric_meter, command: str) -> bytearray | None:
    """Return datas from Electric Meter"""
    command = get_command_mercury(address=electric_meter.TElectricMeter.address, command=command)
    host_port = (str(electric_meter.THost.name), int(electric_meter.TPort.name))
    sock_em = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_em.settimeout(1)
    try:
        sock_em.connect(host_port)
        sock_em.send(command)
        # time.sleep(0)
        received_data = sock_em.recv(128)
    except socket.error:
        received_data = None
    sock_em.close()
    return received_data


def get_connect(electric_meter, command: str) -> bool:
    received_data = exchange_data(electric_meter=electric_meter, command=command)
    if received_data is not None:
        connect = True
    else:
        connect = False
    return connect


def get_verification(electric_meter) -> bool:
    received_data = exchange_data(electric_meter=electric_meter,
                                  command='serial number')
    if received_data is not None:
        unpack_serial = unpack_serial_number(received_data)
        if electric_meter.TElectricMeter.serial != int(unpack_serial):
            verification = False
        else:
            verification = True
    else:
        verification = False
    return verification


def get_data_release(electric_meter) -> bool:
    received_data = exchange_data(electric_meter=electric_meter, command='serial number')
    if received_data is not None:
        data_release = unpack_data_release(received_data)
    else:
        data_release = None
    return data_release


def get_energy(electric_meter, command: str) -> list:
    received_data = exchange_data(electric_meter=electric_meter, command=command)
    if received_data is not None:
        indications = unpack_energy(received_data)
    else:
        indications = None, None, None, None
    return indications
