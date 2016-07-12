# -*- coding: utf-8 -*- #
from django.contrib import admin

from humanos.models import *
from smartcity.admin import SmartCityModelAdmin


class DomicilioAdmin(SmartCityModelAdmin):
    list_display = (
        '__unicode__', 'calle', 'numero_exterior', 'numero_interior', 'colonia',
        'delegacion', 'codigo_postal', 'estado', 'pais'
    )
    list_filter = ('codigo_postal', 'delegacion')


class DiscapacidadInline(admin.StackedInline):
    model = Discapacidad
    radio_fields = {
        'tipo': admin.VERTICAL
    }
    extra = 0


class PersonaAdmin(SmartCityModelAdmin):
    inlines = [DiscapacidadInline]
    list_display = (
        '__unicode__', 'nombre', 'apellido_paterno', 'apellido_materno',
        'genero', 'edad',
    )
    list_filter = ('genero', 'fecha_nacimiento', 'responsables',)
    list_search = ('nombre', 'apellido_paterno', 'apellido_materno',)
    radio_fields = {
        "grupo_sanguineo": admin.HORIZONTAL,
        "rh_sanguineo": admin.HORIZONTAL,
    }
    fieldsets = (
        (u'Datos básicos', {
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno',)
        }),
        ('Datos personales', {
            'classes': ('',),
            'fields': ('fecha_nacimiento', 'lugar_nacimiento'),
        }),
        ('Datos fiscales', {
            'classes': ('collapse',),
            'fields': ('razon_social', 'rfc', 'domicilio_fiscal'),
        }),
        ('Datos médicos', {
            'classes': ('collapse',),
            'fields': ('grupo_sanguineo', 'rh_sanguineo', 'alergias',
                       'fecha_fallecimiento', 'lugar_fallecimiento'),
        }),
    )


class OrganizacionAdmin(SmartCityModelAdmin):
    list_display = ('nombre', 'domicilio', 'rfc')


admin.site.register(Domicilio, DomicilioAdmin)
admin.site.register(Organizacion, OrganizacionAdmin)
admin.site.register(Persona, PersonaAdmin)
