from django.contrib import admin

from .models import Group, Model, Name, Location, TypeConnection, Host, Port, ElectricMeter, Options, Propertys, Periods, \
    Indications


class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class NameAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class TypeConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class PortAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'changed')
    list_display_links = ('name',)
    search_fields = ('name',)


class ElectricMeterAdmin(admin.ModelAdmin):
    list_display = ('model', 'serial', 'host',
                    'polling', 'name', 'generation',
                    'location',
                    )
    list_display_links = ('model', 'serial', 'host',
                          'polling', 'name', 'generation',
                          'location',
                          )
    search_fields = ('serial',)


class OptionsAdmin(admin.ModelAdmin):
    list_display = ('rname', 'created', 'changed')
    list_display_links = ('rname',)
    search_fields = ('rname',)


class PropertysAdmin(admin.ModelAdmin):
    list_display = ('electricmeter', 'options', 'eyear',
                    'emonth', 'eday', 'created', 'changed')
    list_display_links = ('electricmeter', 'options',
                          'eyear', 'emonth', 'eday',)
    search_fields = ('electricmeter', 'options', 'eyear', 'emonth', 'day',)


class PeriodsAdmin(admin.ModelAdmin):
    list_display = ('rname', 'created', 'changed')
    list_display_links = ('rname',)
    search_fields = ('rname',)


class IndicationsAdmin(admin.ModelAdmin):
    list_display = ('electricmeter', 'period',
                    'active_plus', 'active_minus', 'reactive_plus', 'reactive_minus',
                    'created', 'changed')
    list_display_links = ('electricmeter', 'period',
                          'active_plus', 'active_minus', 'reactive_plus', 'reactive_minus',)
    search_fields = ('electricmeter', 'period',
                     'active_plus', 'active_minus', 'reactive_plus', 'reactive_minus',)


admin.site.register(Model, ModelAdmin)
admin.site.register(Name, NameAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(TypeConnection, TypeConnectionAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(ElectricMeter, ElectricMeterAdmin)
# admin.site.register(Options, OptionsAdmin)
# admin.site.register(Propertys, PropertysAdmin)
admin.site.register(Periods, PeriodsAdmin)
admin.site.register(Indications, IndicationsAdmin)
admin.site.register(Group, GroupAdmin)
