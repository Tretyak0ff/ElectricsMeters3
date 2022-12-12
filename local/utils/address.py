

def get_address_model_d(serial: int) -> int:
    address = int(str(serial)[-3:])
    if address < 17:
        if int(str(serial)[-2:]) in range(0, 7):
            address = int(str(serial)[-2:]) + 20
        else:
            address = int(str(serial)[-2:]) + 10
    elif address > 124:
        if int(str(serial)[-2:]) in range(0, 7):
            address = int(str(serial)[-2:]) + 20
        elif int(str(serial)[-2:]) in range(7, 17):
            address = int(str(serial)[-2:]) + 10
        else:
            address = int(str(serial)[-2:])
    else:
        address = int(str(serial)[-3:])
    return address


def get_address_model_not_d(serial: int) -> int:
    address = int(str(serial)[-3:])
    if address < 1:
        address = 1
    elif address > 239:
        if int(str(serial)[-2:]) < 1:
            address = 1
        else:
            address = int(str(serial)[-2:])
    else:
        address = int(str(serial)[-3:])
    return address
