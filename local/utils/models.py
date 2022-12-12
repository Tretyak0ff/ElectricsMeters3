from loguru import logger
from .address import get_address_model_d, get_address_model_not_d


class ElectricMeter:
    @staticmethod
    def get_address(model: str, serial: int) -> int | None:
        if str(model).lower().find('меркурий') == 0:
            if str(model).lower().find('d') == 0:
                return get_address_model_d(serial)
            else:
                return get_address_model_not_d(serial)
        else:
            return None

    def __init__(self,
                 name: str, location: str, model: str, serial: int,
                 typeconnection: str, host: str, port: int, coefficient: int,
                 comments: str, ):
        self.name = name
        self.location = location
        self.model = model
        self.serial = serial

        self.typeconnection = typeconnection
        self.host = host
        self.port = port
        self.address = self.get_address(self.model, self.serial)
        self.coefficient = coefficient

        self.comments = comments

    def __repr__(self):
        return f'{self.name} {self.location} {self.model} {self.serial} ' \
               f'{self.typeconnection} {self.host} {self.port} {self.address}' \
               f'{self.coefficient} ' \
               f'{self.comments}'


