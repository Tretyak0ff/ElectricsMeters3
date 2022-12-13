from ..tables import TElectricMeter


def line_1(electric_meter: TElectricMeter) -> dict:
    data_line = {
        'Location': electric_meter.TLocation.name,
        'Name': electric_meter.TName.name,
        'Model': electric_meter.TModel.name,
        'Serial number': electric_meter.TElectricMeter.serial,
        'Modbus address': electric_meter.TElectricMeter.address,
        'Coefficient': electric_meter.TElectricMeter.coefficient,
    }
    return data_line


def line_2(indications: dict):
    return [
        ('time',
         'active+', 'active-', 'reactive+', 'reactive-'
         ),
        ('year',
         indications.get('energy').get('year').get('active_plus'),
         indications.get('energy').get('year').get('active_minus'),
         indications.get('energy').get('year').get('reactive_plus'),
         indications.get('energy').get('year').get('reactive_minus'),
         ),
        ('month',
         indications.get('energy').get('month').get('active_plus'),
         indications.get('energy').get('month').get('active_minus'),
         indications.get('energy').get('month').get('reactive_plus'),
         indications.get('energy').get('month').get('reactive_minus'),
         ),
        ('day',
         indications.get('energy').get('day').get('active_plus'),
         indications.get('energy').get('day').get('active_minus'),
         indications.get('energy').get('day').get('reactive_plus'),
         indications.get('energy').get('day').get('reactive_minus'),
         ),
    ]


def line_2_reset(indications: dict):
    return [
        ('time',
         'active+', 'active-', 'reactive+', 'reactive-'
         ),
        ('reset',
         indications.get('energy').get('reset').get('active_plus'),
         indications.get('energy').get('reset').get('active_minus'),
         indications.get('energy').get('reset').get('reactive_plus'),
         indications.get('energy').get('reset').get('reactive_minus'),
         ),
    ]
