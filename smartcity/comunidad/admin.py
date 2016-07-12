# -*- coding: utf-8 -*- #
from django.contrib import admin

from comunidad.models import *
from smartcity.admin import SmartCityModelAdmin



class PreferenciaContactoAdmin(SmartCityModelAdmin):
    pass


class PropuestaAdmin(SmartCityModelAdmin):
    pass


class ComentarioAdmin(SmartCityModelAdmin):
    pass


admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Propuesta, PropuestaAdmin)
admin.site.register(PreferenciaContacto, PreferenciaContactoAdmin)
