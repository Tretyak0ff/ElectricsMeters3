
def zero_left_str(message: int) -> str:
    """converting single digit to double digit"""
    if message < 10:
        message = '0' + str(message)
    else:
        message = str(message)
    return message


def unpack_serial_number(message: bytearray) -> str:
    """converts data serial_number"""
    serial_number = zero_left_str(message[1]) + zero_left_str(message[2]) + zero_left_str(message[3]) + zero_left_str(
        message[4])
    return serial_number


def unpack_data_release(message: bytearray) -> str:
    """converts data data_release"""
    data_release = zero_left_str(message[5]) + '.' + zero_left_str(message[6]) + '.' + zero_left_str(message[7])
    return data_release


def unpack_energy(message: bytearray):
    """converts data energy_"""
    active_plus = bytearray()
    active_plus.append(int(message[2]))
    active_plus.append(int(message[1]))
    active_plus.append(int(message[4]))
    active_plus.append(int(message[3]))
    if int.from_bytes(active_plus, "big", signed="True") < 0:
        active_plus = 0
    else:
        active_plus = int.from_bytes(active_plus, "big", signed="True") / 1000

    active_minus = bytearray()
    active_minus.append(int(message[6]))
    active_minus.append(int(message[5]))
    active_minus.append(int(message[8]))
    active_minus.append(int(message[7]))
    if int.from_bytes(active_minus, "big", signed="True") < 0:
        active_minus = 0
    else:
        active_minus = int.from_bytes(active_minus, "big", signed="True")

    reactive_plus = bytearray()
    reactive_plus.append(int(message[10]))
    reactive_plus.append(int(message[9]))
    reactive_plus.append(int(message[12]))
    reactive_plus.append(int(message[11]))
    if int.from_bytes(reactive_plus, "big", signed="True") < 0:
        reactive_plus = 0
    else:
        reactive_plus = int.from_bytes(reactive_plus, "big", signed="True") / 1000

    reactive_minus = bytearray()
    reactive_minus.append(int(message[14]))
    reactive_minus.append(int(message[13]))
    reactive_minus.append(int(message[16]))
    reactive_minus.append(int(message[15]))
    if int.from_bytes(reactive_minus, "big", signed="True") < 0:
        reactive_minus = 0
    else:
        reactive_minus = int.from_bytes(reactive_minus, "big", signed="True") / 1000
    return active_plus, active_minus, reactive_plus, reactive_minus

