# -*- coding: utf-8 -*- #
from django.contrib import admin

from humanos.models import *

class DomicilioAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'calle', 'numero_exterior', 'numero_interior', 'colonia',
        'delegacion', 'codigo_postal', 'estado', 'pais'
    )
    list_filter = ('codigo_postal', 'delegacion')


class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'nombre', 'apellido_paterno', 'apellido_materno',
        'genero', 'fecha_nacimiento', 'edad',
    )
    list_filter = ('genero', 'fecha_nacimiento', 'responsables',)
    list_search = ('nombre', 'apellido_paterno', 'apellido_materno',)
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
        ('Fallecimiento', {
            'classes': ('collapse',),
            'fields': ('fecha_fallecimiento', 'lugar_fallecimiento'),
        }),
    )


class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'domicilio', 'rfc')


admin.site.register(Domicilio, DomicilioAdmin)
admin.site.register(Organizacion, OrganizacionAdmin)
admin.site.register(Persona, PersonaAdmin)
