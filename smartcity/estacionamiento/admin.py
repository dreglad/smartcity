# -*- coding: utf-8 -*- #
from django.contrib import admin

from estacionamiento.models import *
from smartcity.admin import SmartCityModelAdmin


class VehiculoEstacionadoAdmin(SmartCityModelAdmin):
    pass

class VehiculoAdmin(SmartCityModelAdmin):
    list_display = ('placas', 'color', 'modelo', 'marca', 'submarca', 'modelo')


class LugarEstacionamientoAdmin(SmartCityModelAdmin):
    list_display = ('numero_', 'nivel', 'departamento')
    list_filter = (
        ('nivel', admin.RelatedOnlyFieldListFilter),
        'departamento__torre',
        ('departamento', admin.RelatedOnlyFieldListFilter),
        
    )

    def numero_(self, obj):
        return obj.__unicode__()
    numero_.admin_order_field = 'numero'


admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(LugarEstacionamiento, LugarEstacionamientoAdmin)
admin.site.register(VehiculoEstacionado, VehiculoEstacionadoAdmin)
