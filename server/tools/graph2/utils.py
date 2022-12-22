from loguru import logger
from datetime import datetime
from ..models import Indications, ElectricMeter

def get_interval(date_start: datetime, date_stop: datetime) -> str:
    interval = []
    if date_start.month == date_stop.month:
        interval = 'month'
    else:
        interval = 'year'
    return interval


def get_data(date1: str, date2: str) -> dict:
    date_start = None
    date_stop = None
    interval = None
    date1 = datetime.strptime(f'{date1}', '%Y-%m-%d')
    date2 = datetime.strptime(f'{date2}', '%Y-%m-%d')

    if date1 > date2:
        date_start = datetime.strptime(f'{date2.year}-{date2.month}-{date2.day} 00:00', '%Y-%m-%d %H:%M')
        date_stop = datetime.strptime(f'{date1.year}-{date1.month}-{date1.day} 23:59', '%Y-%m-%d %H:%M')
        interval = get_interval(date_start=date_start, date_stop=date_stop)

    if date2 > date1:
        date_start = datetime.strptime(f'{date1.year}-{date1.month}-{date1.day} 00:00', '%Y-%m-%d %H:%M')
        date_stop = datetime.strptime(f'{date2.year}-{date2.month}-{date2.day} 23:59', '%Y-%m-%d %H:%M')
        interval = get_interval(date_start=date_start, date_stop=date_stop)

    if date1 == date2:
        date_start = datetime.strptime(f'{date1.year}-{date1.month}-{date1.day} 00:00', '%Y-%m-%d %H:%M')
        date_stop = datetime.strptime(f'{date2.year}-{date2.month}-{date2.day} 23:59', '%Y-%m-%d %H:%M')
        interval = 'day'

    return {'date_start': date_start,
            'date_stop': date_stop,
            'interval': interval,
    }


def get_energy(date_start: datetime, date_stop: datetime, electricmeter_id: ElectricMeter.pk) -> None | list:
    period = 4
    energy_interval = Indications.objects.distinct('created'). \
        filter(electricmeter_id=electricmeter_id). \
        filter(period_id=period). \
        filter(created__gte=date_start). \
        filter(created__lte=date_stop).all()

    if not energy_interval.exists():
        return None
    else:
        return energy_interval


def get_coordinates(date1: str, date2: str, electricmeter_id: ElectricMeter.pk) -> list:
    date = get_data(date1=date1, date2=date2)
    date_start = date['date_start']
    date_stop = date['date_stop']
    interval = date['interval']
    all_energy = get_energy(date_start=date_start, date_stop=date_stop, electricmeter_id=electricmeter_id)
    coefficient = ElectricMeter.objects.filter(pk=electricmeter_id).last().coefficient

    if all_energy is not None:
        match interval:
            case 'year':
                x_axis = [f'{time.created.month}.{time.created.year}' for time in all_energy
                          if (time.created.day == 1) and (time.created.hour == 0) and (time.created.minute < 15)]
                active_plus = [energy.active_plus * coefficient for energy in all_energy if
                               (energy.created.day == 1) and (energy.created.hour == 0) and (
                                       energy.created.minute < 15)]
                active_minus = [energy.active_minus * coefficient for energy in all_energy if
                                (energy.created.day == 1) and (energy.created.hour == 0) and (
                                        energy.created.minute < 15)]
                reactive_plus = [energy.reactive_plus * coefficient for energy in all_energy if
                                 (energy.created.day == 1) and (energy.created.hour == 0) and (
                                         energy.created.minute < 15)]
                reactive_minus = [energy.reactive_minus * coefficient for energy in all_energy if
                                  (energy.created.day == 1) and (energy.created.hour == 0) and (
                                          energy.created.minute < 15)]
                return x_axis, active_plus, active_minus, reactive_plus, reactive_minus
            case 'month':
                x_axis = [f'{time.created.day}.{time.created.month}.{time.created.year}' for time in all_energy
                          if (time.created.hour == 0) and (time.created.minute < 15)]
                x_axis_delta = [x_axis[i] for i in range(0, len(x_axis) - 1)]

                active_plus = [energy.active_plus * coefficient for energy in all_energy if
                               (energy.created.hour == 0) and (energy.created.minute < 15)]
                active_minus = [energy.active_minus * coefficient for energy in all_energy if
                                (energy.created.hour == 0) and (energy.created.minute < 15)]
                reactive_plus = [energy.reactive_plus * coefficient for energy in all_energy if
                                 (energy.created.hour == 0) and (energy.created.minute < 15)]
                reactive_minus = [energy.reactive_minus * coefficient for energy in all_energy if
                                  (energy.created.hour == 0) and (energy.created.minute < 15)]

                active_plus_delta = [round(active_plus[i] - active_plus[i - 1], 3)
                                     for i in range(1, len(active_plus))]
                active_minus_delta = [round(active_minus[i] - active_minus[i - 1], 3)
                                      for i in range(1, len(active_minus))]
                reactive_plus_delta = [round(reactive_plus[i] - reactive_plus[i - 1], 3)
                                       for i in range(1, len(reactive_plus))]
                reactive_minus_delta = [round(reactive_minus[i] - reactive_minus[i - 1], 3)
                                        for i in range(1, len(reactive_minus))]

                return x_axis_delta, active_plus_delta, active_minus_delta, reactive_plus_delta, reactive_minus_delta
            case 'day':
                x_axis = [f'{(time.created + timedelta(hours=3)).hour}:0{time.created.minute}' for time in
                          all_energy
                          if (time.created.hour > 0) and (time.created.minute == 0)]
                active_plus = [energy.active_plus * coefficient for energy in all_energy
                               if (energy.created.minute == 0)]
                active_minus = [energy.active_minus * coefficient for energy in all_energy
                                if (energy.created.minute == 0)]
                reactive_plus = [energy.reactive_plus * coefficient for energy in all_energy
                                 if (energy.created.minute == 0)]
                reactive_minus = [energy.reactive_minus * coefficient for energy in all_energy
                                  if (energy.created.minute == 0)]

                active_plus_delta = [round(active_plus[i] - active_plus[i - 1], 3)
                                     for i in range(1, len(active_plus))]
                active_minus_delta = [round(active_minus[i] - active_minus[i - 1], 3)
                                      for i in range(1, len(active_minus))]
                reactive_plus_delta = [round(reactive_plus[i] - reactive_plus[i - 1], 3)
                                       for i in range(1, len(reactive_plus))]
                reactive_minus_delta = [round(reactive_minus[i] - reactive_minus[i - 1], 3)
                                        for i in range(1, len(reactive_minus))]

                return x_axis, active_plus_delta, active_minus_delta, reactive_plus_delta, reactive_minus_delta
    else:
        x_axis = []
        active_plus = []
        active_minus = []
        reactive_plus = []
        reactive_minus = []
        return x_axis, active_plus, active_minus, reactive_plus, reactive_minus



