import calendar
from datetime import datetime
from django.shortcuts import render
from django.views.generic.edit import CreateView
from loguru import logger

from .models import ElectricMeter, Location, Propertys
from .forms import LocationForm, ReportForm, IntervalForm
from .utils import get_energy_last, get_graph_coordinates, get_report_indications
from .report2.utils import get_report2


class LocationCreateView(CreateView):
    template_name = 'tools/create.html'
    form_class = LocationForm
    success_url = '/tools/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Locations'] = Location.objects.all()
        return context


def index(request) -> render:
    ems = ElectricMeter.objects.all()
    context = {'ems': ems,
               }
    return render(request, 'tools/index.html', context)


def report(request) -> render:
    report_form = ReportForm(request.POST or None)
    indications = []
    indications_len = 0
    if report_form.is_valid():
        indications = get_report_indications(
            selected_year=report_form.cleaned_data.get("years"),
            selected_month=report_form.cleaned_data.get("months"),
            selected_coefficient=report_form.cleaned_data.get("coefficient"),
        )
        indications_len = range(len(indications))

    context = {'form': report_form,
               'indications': indications,
               # 'indications_len': indications_len,
               }
    return render(request, 'tools/report.html', context)


def report2(request) -> render:
    report_form = ReportForm(request.POST or None)
    energy_generations = []
    if report_form.is_valid():
        energy_generations, energy_consumptions = get_report2(
            selected_year=report_form.cleaned_data.get("years"),
            selected_month=report_form.cleaned_data.get("months"),
            selected_coefficient=report_form.cleaned_data.get("coefficient"), )

        logger.debug(energy_generations)
    context = {'form': report_form,
               'generations': energy_generations,

               # 'indications': power_generation,
               # 'indications_len': indications_len,
               }
    return render(request, 'tools/report2.html', context)


def by_location(request, location_id) -> render:
    ems = ElectricMeter.objects.filter(location_id=location_id)
    context = {'ems': ems,
               }
    return render(request, 'tools/location.html', context)


def by_electricmeter(request, location_id, electricmeter_id: ElectricMeter) -> render:
    ems = ElectricMeter.objects.filter(pk=electricmeter_id)
    energy = get_energy_last(electricmeter_id)
    x_axis, graph_1, graph_2, graph_3, graph_4 = [], [], [], [], []
    interval_form = IntervalForm(request.POST or None)
    selected_interval = interval_form.data.get('interval_radio')
    if interval_form.is_valid():
        x_axis, graph_1, graph_2, graph_3, graph_4 = get_graph_coordinates(
            selected_interval=selected_interval,
            electricmeter_id=electricmeter_id
        )

    context = {'ems': ems,
               'energy': energy,
               'form': interval_form,
               'x_axis': x_axis,
               'graph_1': graph_1,
               'graph_2': graph_2,
               'graph_3': graph_3,
               'graph_4': graph_4,
               }

    return render(request, 'tools/electricmeter.html', context)
