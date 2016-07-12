# -*- coding: utf-8 -*- #
from django.contrib import admin

from condominios.models import *
from smartcity.admin import SmartCityModelAdmin




class ArrendamientoAdmin(SmartCityModelAdmin):
    pass


class DepartamentoAdmin(SmartCityModelAdmin):
    list_display = (
        '__unicode__', 'torre', 'nivel', 'numero_display', 'superficie', 'recamaras',
    )
    list_filter = (
        'torre',
        ('nivel', admin.RelatedOnlyFieldListFilter),
        'numero'
    )


class DesarrolloAdmin(SmartCityModelAdmin):
    list_display = ('nombre', 'domicilio',)


class NivelAdmin(SmartCityModelAdmin):
    list_display = ('nombre', 'identificador', 'numero', 'desarrollo')


class TorreAdmin(SmartCityModelAdmin):
    list_display = ('identificador', 'desarrollo')



class PropiedadAdmin(SmartCityModelAdmin):
    list_display = ('departamento', 'propietario', 'fecha_inicio', 'fecha_termino')
    list_filter = ('propietario', 'departamento', 'fecha_inicio', 'fecha_termino')



admin.site.register(Arrendamiento, ArrendamientoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Desarrollo, DesarrolloAdmin)
admin.site.register(Nivel, NivelAdmin)
admin.site.register(Propiedad, PropiedadAdmin)
admin.site.register(Torre, TorreAdmin)
