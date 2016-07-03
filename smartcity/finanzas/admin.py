# -*- coding: utf-8 -*- #
from django.contrib import admin

from finanzas.models import *


class CuentaBancariaAdmin(admin.ModelAdmin):
    pass


admin.site.register(CuentaBancaria, CuentaBancariaAdmin)

