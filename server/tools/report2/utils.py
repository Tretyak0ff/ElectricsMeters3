from loguru import logger
import calendar
from datetime import datetime, timedelta
import dateutil.relativedelta
from ..models import Propertys, ElectricMeter, Periods, Indications
from ..utils import model_modbus, model_reset


def get_indications(electricmeter_id: int, coefficient: int,
                    created_start: datetime, created_stop: datetime) -> Indications | None:
    ind_first = Indications.objects. \
        filter(electricmeter=electricmeter_id).filter(period=4).order_by('created'). \
        filter(created__gte=created_start).filter(created__lte=created_stop). \
        filter(active_plus__isnull=False).first()
    ind_last = Indications.objects. \
        filter(electricmeter=electricmeter_id).filter(period=4).order_by('created'). \
        filter(created__gte=created_start).filter(created__lte=created_stop). \
        filter(active_plus__isnull=False).last()

    if ind_first and ind_last:
        energy = Indications(
            electricmeter_id=electricmeter_id, period_id=4,
            active_plus=round((ind_last.active_plus - ind_first.active_plus) * coefficient, 1),
            active_minus=round((ind_last.active_minus - ind_first.active_minus) * coefficient, 1),
            reactive_plus=round((ind_last.reactive_plus - ind_first.reactive_plus) * coefficient, 1),
            reactive_minus=round((ind_last.reactive_minus - ind_first.reactive_minus) * coefficient, 1),
            created=datetime.now(), changed=datetime.now())
    else:
        energy = None
    return energy


def get_report2(selected_year: str, selected_month: str, selected_coefficient: bool) -> tuple:
    energy_generation = []
    energy_consumption = []
    crt_start = datetime.strptime(f'{int(selected_year)}-{int(selected_month)}', '%Y-%m')
    crt_stop = datetime.strptime(f'{int(crt_start.year)}-{int(crt_start.month)}-'
                                 f'{calendar.monthrange(int(crt_start.year), int(crt_start.month))[1]} '
                                 f'23:59', '%Y-%m-%d %H:%M')

    prev_start = crt_start + dateutil.relativedelta.relativedelta(months=-1)
    prev_stop = datetime.strptime(f'{int(prev_start.year)}-{int(prev_start.month)}-'
                                  f'{calendar.monthrange(int(prev_start.year), int(prev_start.month))[1]} '
                                  f'23:59', '%Y-%m-%d %H:%M')

    electricmeter_id_generation = [g['id'] for g in ElectricMeter.objects.values('id').filter(generation=True).all()]
    for electricmeter_id in Indications.objects.values('electricmeter').distinct('electricmeter').all():

        if selected_coefficient:
            coefficient = ElectricMeter.objects.filter(pk=electricmeter_id['electricmeter']).last().coefficient
        else:
            coefficient = 1

        if electricmeter_id['electricmeter'] in electricmeter_id_generation:

            energy_previous = get_indications(electricmeter_id=electricmeter_id['electricmeter'],
                                              coefficient=coefficient,
                                              created_start=prev_start, created_stop=prev_stop)
            energy_current = get_indications(electricmeter_id=electricmeter_id['electricmeter'],
                                             coefficient=coefficient,
                                             created_start=crt_start, created_stop=crt_stop)
            try:
                energy_percent = round(energy_current.active_plus / energy_previous.active_plus * 100, 1)
            except:
                energy_percent = None

            energy_generation.append({'previous': energy_previous,
                                      'current': energy_current,
                                      'percent': energy_percent})
        else:
            energy_previous = get_indications(electricmeter_id=electricmeter_id['electricmeter'],
                                              coefficient=coefficient,
                                              created_start=prev_start, created_stop=prev_stop)
            energy_current = get_indications(electricmeter_id=electricmeter_id['electricmeter'],
                                             coefficient=coefficient,
                                             created_start=crt_start, created_stop=crt_stop)
            try:
                energy_percent = round(energy_current.active_plus / energy_previous.active_plus * 100, 1)
            except:
                energy_percent = None

            energy_consumption.append({'previous': energy_previous,
                                       'current': energy_current,
                                       'percent': energy_percent})
    return energy_generation, energy_consumption

