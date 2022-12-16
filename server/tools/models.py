from datetime import datetime
from django.db import models


# Create your models here.
class Name(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование узла')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Наименования узлов'
        verbose_name = 'Наименование узла'
        ordering = ['-name']


class Location(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Место установки')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Места установки'
        verbose_name = 'Место установки'
        ordering = ['-name']


class Model(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Модель электросчетчика')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Модели электросчетчиков'
        verbose_name = 'Модель электросчетчика'
        ordering = ['-name']


class TypeConnection(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Тип соединения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Типы соединений'
        verbose_name = 'Тип соединения'
        ordering = ['-name']


class Host(models.Model):
    name = models.CharField(max_length=16, db_index=True, verbose_name='IP-адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'IP-адресса'
        verbose_name = 'IP-адрес'
        ordering = ['-name']


class Port(models.Model):
    name = models.PositiveIntegerField(db_index=True, verbose_name='IP-порт')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'IP-порты'
        verbose_name = 'IP-порт'
        ordering = ['-name']


class Group(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Группа электросчетчика')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Группы электросчетчиков'
        verbose_name = 'Группа электросчетчика'
        ordering = ['-name']


class ElectricMeter(models.Model):
    group = models.ForeignKey('Group', null=True, on_delete=models.PROTECT, verbose_name='Наименование группы')
    name = models.ForeignKey('Name', null=True, on_delete=models.PROTECT, verbose_name='Наименование узла')
    location = models.ForeignKey('Location', null=True, on_delete=models.PROTECT, verbose_name='Место установки')
    model = models.ForeignKey('Model', null=True, on_delete=models.PROTECT, verbose_name='Модель электросчетчика')
    serial = models.PositiveIntegerField(null=True, verbose_name='Серийный номер электросчетчика')

    typeconnection = models.ForeignKey('TypeConnection', blank=True, null=True, on_delete=models.PROTECT,
                                       verbose_name='Тип соединения')
    host = models.ForeignKey('Host', blank=True, null=True, on_delete=models.PROTECT, verbose_name='IP-адрес')
    port = models.ForeignKey('Port', blank=True, null=True, on_delete=models.PROTECT, verbose_name='IP-порт')
    address = models.PositiveIntegerField(null=True, verbose_name='ModBus адрес')

    coefficient = models.PositiveIntegerField(null=True, verbose_name='Коэфициент трансформации')
    polling = models.BooleanField(blank=False, null=False, verbose_name='Опрос устройства')
    generation = models.BooleanField(blank=False, null=False, verbose_name='Выработка электроэнергии')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.model} №{self.serial}'

    class Meta:
        verbose_name_plural = 'Электросчетчики'
        verbose_name = 'Электросчетчик'
        ordering = ['-model', '-name', '-location',
                    '-serial', '-typeconnection', '-host',
                    '-port']


class Options(models.Model):
    name = models.CharField(max_length=16, db_index=True, verbose_name='Параметр')
    rname = models.CharField(max_length=100, null=True, db_index=True, verbose_name='Наименование параметра')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.rname}'

    class Meta:
        verbose_name_plural = 'Параметры'
        verbose_name = 'Параметр'
        ordering = ['-rname']


class Propertys(models.Model):
    electricmeter = models.ForeignKey('ElectricMeter', null=True, on_delete=models.PROTECT,
                                      verbose_name='Электросчетчик')
    options = models.ForeignKey('Options', null=True, on_delete=models.PROTECT, verbose_name='Параметр энергии')
    eyear = models.FloatField(null=True, verbose_name='Накопленная энергия за год')
    emonth = models.FloatField(null=True, verbose_name='Накопленная энергия за месяц')
    eday = models.FloatField(null=True, verbose_name='Накопленная энергия день')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.electricmeter} ' \
               f'{self.options} ' \
               f'{self.eyear} ' \
               f'{self.eday} ' \
               f'{self.eday}' \
               f'{self.created}' \
               f'{self.changed}'

    class Meta:
        verbose_name_plural = 'Показания'
        verbose_name = 'Показания'
        ordering = ''


class Periods(models.Model):
    name = models.CharField(max_length=16, db_index=True, verbose_name='Интервал времени')
    rname = models.CharField(max_length=100, null=True, db_index=True, verbose_name='Наименование интервала времени')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.rname}'

    class Meta:
        verbose_name_plural = 'Интервалы времени'
        verbose_name = 'Интервал времени'
        ordering = ['-rname']


class Indications(models.Model):
    electricmeter = models.ForeignKey('ElectricMeter', null=True, on_delete=models.PROTECT,
                                      verbose_name='Электросчетчик')
    period = models.ForeignKey('Periods', null=True, on_delete=models.PROTECT, verbose_name='Интервал времени')
    active_plus = models.FloatField(null=True, verbose_name='Положительная активная энергия')
    active_minus = models.FloatField(null=True, verbose_name='Отрицательная активная энергия')
    reactive_plus = models.FloatField(null=True, verbose_name='Положительная реактивная энергия')
    reactive_minus = models.FloatField(null=True, verbose_name='Отрицательная реактивная энергия')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed = models.DateTimeField(default=datetime.now, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return f'{self.electricmeter} ' \
               f'{self.period} ' \
               f'{self.active_plus} ' \
               f'{self.active_minus} ' \
               f'{self.reactive_plus}' \
               f'{self.reactive_minus}' \
               f'{self.created}' \
               f'{self.changed}'

    class Meta:
        verbose_name_plural = 'Показания электроэнергии'
        verbose_name = 'Показание электроэнергии'
        ordering = ''
