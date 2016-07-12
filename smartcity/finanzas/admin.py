# -*- coding: utf-8 -*- #
from django.contrib import admin

from finanzas.models import *
from smartcity.admin import SmartCityModelAdmin


class CuentaBancariaAdmin(SmartCityModelAdmin):
    pass
    #lista_display = ('__unicode__', 'banco', 'clabe', 'beneficiario')


class ReciboAdmin(SmartCityModelAdmin):
    list_display = ('clave', 'nombre')


class ProveedorAdmin(SmartCityModelAdmin):
    pass

class ReciboAdmin(SmartCityModelAdmin):
    pass

class ServicioAdmin(SmartCityModelAdmin):
    pass

class BancoAdmin(SmartCityModelAdmin):
    pass

class CuotaAdmin(SmartCityModelAdmin):
    pass

class PagoCuotaAdmin(SmartCityModelAdmin):
    pass


#admin.site.register(Banco, BancoAdmin)
admin.site.register(CuentaBancaria, CuentaBancariaAdmin)
admin.site.register(Cuota, CuotaAdmin)
admin.site.register(PagoCuota, PagoCuotaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Recibo, ReciboAdmin)
admin.site.register(Servicio, ServicioAdmin)


