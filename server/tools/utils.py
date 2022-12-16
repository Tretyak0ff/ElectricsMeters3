from loguru import logger
import calendar
import dateutil.relativedelta
from datetime import datetime, timedelta
from .models import Propertys, ElectricMeter, Periods, Indications


model_modbus = ('Панель PCC33MLD',)
model_reset = ('Меркурий-230 AR-00 R',)


def get_energy_last_old(electricmeter_id: ElectricMeter.pk) -> dict:
    active_plus = Propertys.objects.filter(electricmeter_id=electricmeter_id). \
        filter(options=1).last()
    active_minus = Propertys.objects.filter(electricmeter_id=electricmeter_id). \
        filter(options=2).last()
    reactive_plus = Propertys.objects.filter(electricmeter_id=electricmeter_id). \
        filter(options=3).last()
    reactive_minus = Propertys.objects.filter(electricmeter_id=electricmeter_id). \
        filter(options=4).last()
    return {
        'active_plus': active_plus,
        'active_minus': active_minus,
        'reactive_plus': reactive_plus,
        'reactive_minus': reactive_minus
    }


def get_energy_calc(electricmeter_id: ElectricMeter.pk, energy: Indications) -> Indications:
    coefficient = ElectricMeter.objects.filter(pk=electricmeter_id).last().coefficient
    energy_calc = Indications(
        electricmeter_id=energy.electricmeter_id,
        period_id=energy.period.id,
        active_plus=round(energy.active_plus * coefficient, 3),
        active_minus=round(energy.active_minus * coefficient, 3),
        reactive_plus=round(energy.reactive_plus * coefficient, 3),
        reactive_minus=round(energy.reactive_minus * coefficient, 3),
        created=energy.created,
        changed=energy.changed
    )
    return energy_calc


def get_energy_last(electricmeter_id: ElectricMeter.pk) -> list:
    if str(ElectricMeter.objects.filter(pk=electricmeter_id).last().model) in model_modbus or model_reset:
        energy_reset = Indications.objects.filter(electricmeter_id=electricmeter_id). \
            filter(period_id=Periods.objects.filter(name='reset').last().pk).last()
        if energy_reset is not None:
            energy_reset_calc = get_energy_calc(electricmeter_id=electricmeter_id, energy=energy_reset)
            energy = [energy_reset_calc, ]
        else:
            energy = []
    else:
        energy_year = Indications.objects.filter(electricmeter_id=electricmeter_id). \
            filter(period_id=Periods.objects.filter(name='year').last().pk).last()
        energy_month = Indications.objects.filter(electricmeter_id=electricmeter_id). \
            filter(period_id=Periods.objects.filter(name='month').last().pk).last()
        energy_day = Indications.objects.filter(electricmeter_id=electricmeter_id). \
            filter(period_id=Periods.objects.filter(name='day').last().pk).last()

        if energy_year or energy_month or energy_day is not None:
            energy_year_calc = get_energy_calc(electricmeter_id=electricmeter_id, energy=energy_year)
            energy_month_calc = get_energy_calc(electricmeter_id=electricmeter_id, energy=energy_month)
            energy_day_calc = get_energy_calc(electricmeter_id=electricmeter_id, energy=energy_day)

            energy = [energy_year_calc,
                      energy_month_calc,
                      energy_day_calc,
                      ]
        else:
            energy = []
    return energy


def get_bag_data(selected_interval: str, electricmeter_id: ElectricMeter.pk, options: int) -> list | None:
    match selected_interval:
        case 'day':
            date_after = datetime.strptime(f'{datetime.now().date()} '
                                           f'00:00', '%Y-%m-%d %H:%M')
        case 'month':
            date_after = datetime.strptime(f'{datetime.now().date().year}-{datetime.now().date().month}-'
                                           f'01 00:00', '%Y-%m-%d %H:%M')
        case 'year':
            date_after = datetime.strptime(f'{datetime.now().date().year}'
                                           f'-01-01 00:00', '%Y-%m-%d %H:%M')
    energy_interval = Propertys.objects.distinct('created'). \
        filter(electricmeter_id=electricmeter_id). \
        filter(options=options).filter(created__gte=date_after). \
        filter(created__lte=datetime.now()).all()

    if not energy_interval.exists():
        return None
    else:
        return energy_interval


def get_energy(selected_interval: str, electricmeter_id: ElectricMeter.pk) -> None | list:
    if str(ElectricMeter.objects.filter(pk=electricmeter_id).last().model) in (model_modbus or model_reset):
        period = 4
        match selected_interval:
            case 'year':
                date_after = datetime.strptime(f'{datetime.now().date().year}'
                                               f'-01-01 00:00', '%Y-%m-%d %H:%M')
            case 'month':
                date_after = datetime.strptime(f'{datetime.now().date().year}-{datetime.now().date().month}-'
                                               f'01 00:00', '%Y-%m-%d %H:%M')
            case 'day':
                date_after = (datetime.strptime(f'{datetime.now().date()} '
                                                f'00:00', '%Y-%m-%d %H:%M')) - timedelta(hours=3)
    else:
        match selected_interval:
            case 'year':
                date_after = datetime.strptime(f'{datetime.now().date().year}'
                                               f'-01-01 00:00', '%Y-%m-%d %H:%M')
                period = 1
            case 'month':
                date_after = datetime.strptime(f'{datetime.now().date().year}-{datetime.now().date().month}-'
                                               f'01 00:00', '%Y-%m-%d %H:%M')
                period = 2
            case 'day':
                date_after = datetime.strptime(f'{datetime.now().date()} '
                                               f'00:00', '%Y-%m-%d %H:%M') - timedelta(hours=3)
                period = 2

    energy_interval = Indications.objects.distinct('created'). \
        filter(electricmeter_id=electricmeter_id). \
        filter(period_id=period). \
        filter(created__gte=date_after). \
        filter(created__lte=datetime.now()).all()

    if not energy_interval.exists():
        return None
    else:
        return energy_interval


def get_graph_options(selected_interval: str, electricmeter_id: ElectricMeter.pk):
    active_plus = get_bag_data(selected_interval=selected_interval, electricmeter_id=electricmeter_id, options=1)
    active_minus = get_bag_data(selected_interval=selected_interval, electricmeter_id=electricmeter_id, options=2)
    reactive_plus = get_bag_data(selected_interval=selected_interval, electricmeter_id=electricmeter_id, options=3)
    reactive_minus = get_bag_data(selected_interval=selected_interval, electricmeter_id=electricmeter_id, options=4)

    if active_plus or active_minus or reactive_plus or reactive_minus is not None:
        match selected_interval:
            case 'day':
                x_axis = [f'{propertys.created.hour}:0{propertys.created.minute}' for propertys in active_plus
                          if (propertys.created.minute == 0)]
                graph_1 = [propertys.eday for propertys in active_plus if (propertys.created.minute == 0)]
                graph_2 = [propertys.eday for propertys in active_minus if (propertys.created.minute == 0)]
                graph_3 = [propertys.eday for propertys in reactive_plus if (propertys.created.minute == 0)]
                graph_4 = [propertys.eday for propertys in reactive_minus if (propertys.created.minute == 0)]
                return x_axis, graph_1, graph_2, graph_3, graph_4
            case 'month':
                x_axis = [f'{propertys.created.day}.{propertys.created.month}.{propertys.created.year}'
                          for propertys in active_plus
                          if (propertys.created.hour == 0) and (propertys.created.minute < 15)]
                graph_1 = [propertys.emonth
                           for propertys in active_plus
                           if (propertys.created.hour == 0) and (propertys.created.minute < 15)]
                graph_2 = [propertys.emonth
                           for propertys in active_minus
                           if (propertys.created.hour == 0) and (propertys.created.minute < 15)]
                graph_3 = [propertys.emonth
                           for propertys in reactive_plus
                           if (propertys.created.hour == 0) and (propertys.created.minute < 15)]
                graph_4 = [propertys.emonth
                           for propertys in reactive_minus
                           if ((propertys.created.hour == 0) and (propertys.created.minute < 15))]
                return x_axis, graph_1, graph_2, graph_3, graph_4
            case 'year':
                x_axis = [f'{propertys.created.day}.{propertys.created.month}.{propertys.created.year}'
                          for propertys in active_plus
                          if (propertys.created.day == 1) and
                          (propertys.created.hour == 00) and
                          (propertys.created.minute < 15)]
                graph_1 = [propertys.eyear for propertys in active_plus
                           if (propertys.created.day == 1) and
                           (propertys.created.hour == 00) and
                           (propertys.created.minute < 15)]
                graph_2 = [propertys.eyear for propertys in active_minus
                           if (propertys.created.day == 1) and
                           (propertys.created.hour == 00) and
                           (propertys.created.minute < 15)]
                graph_3 = [propertys.eyear for propertys in reactive_plus
                           if (propertys.created.day == 1) and
                           (propertys.created.hour == 00) and
                           (propertys.created.minute < 15)]
                graph_4 = [propertys.eyear for propertys in reactive_minus
                           if (propertys.created.day == 1) and
                           (propertys.created.hour == 00) and
                           (propertys.created.minute < 15)]
                return x_axis, graph_1, graph_2, graph_3, graph_4
    else:
        return [], [], [], [], []


def get_graph_coordinates(selected_interval: str, electricmeter_id: ElectricMeter.pk) -> list:
    all_energy = get_energy(selected_interval, electricmeter_id)
    coefficient = ElectricMeter.objects.filter(pk=electricmeter_id).last().coefficient
    if all_energy is not None:
        match selected_interval:
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
                x_axis = [f'{(time.created + timedelta(hours=3)).hour}:0{time.created.minute}' for time in all_energy
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


def get_report_indications(selected_year: str, selected_month: str, selected_coefficient: bool) -> list[dict]:
    indications = []
    crt_start = datetime.strptime(f'{int(selected_year)}-{int(selected_month)}', '%Y-%m')
    prev_start = crt_start + dateutil.relativedelta.relativedelta(months=-1)

    crt_stop = datetime.strptime(f'{int(crt_start.year)}-{int(crt_start.month)}-'
                                 f'{calendar.monthrange(int(crt_start.year), int(crt_start.month))[1]} '
                                 f'23:59', '%Y-%m-%d %H:%M')
    prev_stop = datetime.strptime(f'{int(prev_start.year)}-{int(prev_start.month)}-'
                                  f'{calendar.monthrange(int(prev_start.year), int(prev_start.month))[1]} '
                                  f'23:59', '%Y-%m-%d %H:%M')
    for electricmeter_id in Indications.objects.values('electricmeter').distinct('electricmeter'):
        if str(ElectricMeter.objects.filter(pk=electricmeter_id['electricmeter']).last().model) in (model_modbus or
                                                                                                    model_reset):
            period = 4
        else:
            period = 1

        indications_crt_first = Indications.objects.filter(electricmeter=electricmeter_id['electricmeter']). \
            filter(period=period).filter(created__gte=crt_start).filter(created__lte=crt_stop).first()
        indications_crt_last = Indications.objects.filter(electricmeter=electricmeter_id['electricmeter']). \
            filter(period=period).filter(created__gte=crt_start).filter(created__lte=crt_stop).last()

        indications_prev_first = Indications.objects.filter(electricmeter=electricmeter_id['electricmeter']). \
            filter(period=period).filter(created__gte=prev_start).filter(created__lte=prev_stop).first()
        indications_prev_last = Indications.objects.filter(electricmeter=electricmeter_id['electricmeter']). \
            filter(period=period).filter(created__gte=prev_start).filter(created__lte=prev_stop).last()

        if selected_coefficient:
            coefficient = ElectricMeter.objects.filter(pk=electricmeter_id['electricmeter']).last().coefficient
        else:
            coefficient = 1

        if indications_crt_first and indications_crt_last is not None:
            energy_crt = Indications(
                electricmeter_id=electricmeter_id['electricmeter'], period_id=period,
                active_plus=round(
                    (indications_crt_last.active_plus - indications_crt_first.active_plus) * coefficient, 1),
                active_minus=round(
                    (indications_crt_last.active_minus - indications_crt_first.active_minus) * coefficient, 1),
                reactive_plus=round(
                    (indications_crt_last.reactive_plus - indications_crt_first.reactive_plus) * coefficient, 1),
                reactive_minus=round(
                    (indications_crt_last.reactive_minus - indications_crt_first.reactive_minus) * coefficient, 1),
                created=datetime.now(), changed=datetime.now())
            if indications_prev_first and indications_prev_last is not None:
                energy_prev = Indications(
                    electricmeter_id=electricmeter_id['electricmeter'], period_id=period,
                    active_plus=round(
                        (indications_prev_last.active_plus - indications_prev_first.active_plus) * coefficient, 1),
                    active_minus=round(
                        (indications_prev_last.active_minus - indications_prev_first.active_minus) * coefficient, 1),
                    reactive_plus=round(
                        (indications_prev_last.reactive_plus - indications_prev_first.reactive_plus) * coefficient, 1),
                    reactive_minus=round(
                        (indications_prev_last.reactive_minus - indications_prev_first.reactive_minus) * coefficient,
                        1),
                    created=datetime.now(), changed=datetime.now())
                try:
                    energy_pct = round(energy_crt.active_plus / energy_prev.active_plus * 100, 1)
                except:
                    energy_pct = None
            else:
                energy_prev = None
                energy_pct = None
            indications.append({'prev': energy_prev,
                                'crt': energy_crt,
                                'pct': energy_pct})
    return indications
