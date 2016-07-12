# -*- coding: utf-8 -*- #
from django.contrib import admin

from seguridad.models import *
from smartcity.admin import SmartCityModelAdmin



class ReporteAdmin(SmartCityModelAdmin):
    pass
    #list_display = ('nombre', 'domicilio', 'rfc')


class VisitaAdmin(SmartCityModelAdmin):
    pass
    #list_display = ('nombre', 'domicilio', 'rfc')


admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Visita, VisitaAdmin)
