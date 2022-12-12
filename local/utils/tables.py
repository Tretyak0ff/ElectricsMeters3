from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TName(Base):
    __tablename__ = 'tools_name'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(100), comment='name node')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    tools_electricmeter = relationship('TElectricMeter')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.created} {self.changed}'


class TLocation(Base):
    __tablename__ = 'tools_location'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(100), comment='install location')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    tools_electricmeter = relationship('TElectricMeter')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.created} {self.changed}'


class TModel(Base):
    __tablename__ = 'tools_model'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(100), comment='model of electric meter')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    tools_electricmeter = relationship('TElectricMeter')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.created} {self.changed}'


class TTypeConnection(Base):
    __tablename__ = 'tools_typeconnection'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(100), comment='type connection')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    tools_electricmeter = relationship('TElectricMeter')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.created} {self.changed}'


class THost(Base):
    __tablename__ = 'tools_host'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(16), comment='IP-address')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    tools_electricmeter = relationship('TElectricMeter')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.created} {self.changed}'


class TPort(Base):
    __tablename__ = 'tools_port'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True)
    name = Column(Integer(), comment='IP-port')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    tools_electricmeter = relationship('TElectricMeter')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.created} {self.changed}'


class TElectricMeter(Base):
    __tablename__ = 'tools_electricmeter'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True )

    name_id = Column(Integer(), ForeignKey('tools_name.id'), comment='ID name node')
    location_id = Column(Integer(), ForeignKey('tools_location.id'), comment='ID install location')
    model_id = Column(Integer(), ForeignKey('tools_model.id'), comment='ID get_model electric meter')
    serial = Column(Integer(), comment='serial number electric meter')

    typeconnection_id = Column(Integer(), ForeignKey('tools_typeconnection.id'), comment='ID type connection')
    host_id = Column(Integer(), ForeignKey('tools_host.id'), comment='ID IP-address')
    port_id = Column(Integer(), ForeignKey('tools_port.id'), comment='ID IP-port')
    address = Column(Integer(), comment='modbus address of electric meter')

    coefficient = Column(Integer(), comment='coefficient transformation of electric meter')
    polling = Column(Boolean(), comment='polling electric meter')
    generation = Column(Boolean(), comment='power generation electric meter')

    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    def __repr__(self):
        return f'{self.id} ' \
               f'{self.model_id} {self.name_id} {self.location_id} {self.serial} ' \
               f'{self.typeconnection_id} {self.host_id}  {self.port_id} {self.coefficient}' \
               f'{self.polling} ' \
               f'{self.created} {self.changed}'


class TPropertys(Base):
    __tablename__ = 'tools_propertys'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True)

    electricmeter_id = Column(Integer(), ForeignKey('tools_electricmeter.id'), comment='electric meter ID')
    options_id = Column(Integer(), ForeignKey('tools_options.id'), comment='options of electric meter ID')
    eyear = Column(Float(), comment='energy of year')
    emonth = Column(Float(), comment='energy of month')
    eday = Column(Float(), comment='energy of day')

    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    def __repr__(self) -> str:
        return f'{self.id} {self.electricmeter_id} {self.options_id} ' \
               f'{self.eyear} {self.emonth} {self.eday} ' \
               f'{self.created} {self.changed}'


class TOptions(Base):
    __tablename__ = 'tools_options'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True )

    name = Column(String(16), comment='Parameter')
    rname = Column(String(100), comment='RU Parameter')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.rname} {self.created} {self.changed}'


class TPeriods(Base):
    __tablename__ = 'tools_periods'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True)

    name = Column(String(16), comment='Period')
    rname = Column(String(100), comment='Period RU')
    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    def __repr__(self) -> str:
        return f'{self.id} {self.name} {self.rname} {self.created} {self.changed}'


class TIndications(Base):
    __tablename__ = 'tools_indications'

    id = Column(Integer, nullable=True, unique=True, primary_key=True, autoincrement=True)

    electricmeter_id = Column(Integer(), ForeignKey('tools_electricmeter.id'), comment='electric meter ID')
    period_id = Column(Integer(), ForeignKey('tools_periods.id'), comment='time periods ID')
    active_plus = Column(Float(), comment='active positive energy')
    active_minus = Column(Float(), comment='active negative energy')
    reactive_plus = Column(Float(), comment='reactive positive energy')
    reactive_minus = Column(Float(), comment='reactive negative energy')

    created = Column(DateTime(), comment='date of creation')
    changed = Column(DateTime(), comment='date of modification')

    def __repr__(self) -> str:
        return f'{self.id} {self.electricmeter_id} {self.period_id} ' \
               f'{self.active_plus} {self.active_minus} {self.reactive_plus} {self.reactive_minus} ' \
               f'{self.created} {self.changed}'
