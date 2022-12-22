import calendar
import locale
from django import forms
from django.forms import ModelForm

from .models import Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('name',)


class ReportForm(forms.Form):
    MONTHS = (
        ('', ''),
        ('01', 'Январь'),
        ('02', 'Февраль'),
        ('03', 'Март'),
        ('04', 'Апрель'),
        ('05', 'Май'),
        ('06', 'Июнь'),
        ('07', 'Июль'),
        ('08', 'Август'),
        ('09', 'Сентябрь'),
        ('10', 'Октябрь'),
        ('11', 'Ноябрь'),
        ('12', 'Декабрь'),
    )

    months = forms.ChoiceField(
        choices=MONTHS,
        label='Месяц',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    YEARS = (
        ('', ''),
        ('2022', '2022'),
        # ('2023', '2023'),
    )

    years = forms.ChoiceField(
        choices=YEARS,
        label='Год',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    coefficient = forms.BooleanField(
        required=False,
        label='Коэффициент трансформации',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class IntervalForm(forms.Form):
    interval_radio = forms.ChoiceField(
        choices=(
            ('year', 'За год'),
            # ('02', 'Неделя'),
            ('month', 'За месяц'),
            # ('04', 'Квартал'),
            ('day', 'За день'),
        ),
        label='Период',
        widget=forms.RadioSelect(attrs={'class': 'btn-check', 'onchange': 'form.submit()'})
    )


class DateInputForm(forms.Form):
    previous = forms.DateField(
            label='C',
            widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        )
    current = forms.DateField(
            label='По',
            widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        )