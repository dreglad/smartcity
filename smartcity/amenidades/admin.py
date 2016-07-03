# -*- coding: utf-8 -*- #
from django.contrib import admin

from amenidades.models import *


class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'tipo',
    )
    list_filter = ('tipo',)


class ReglaInline(admin.StackedInline):
    """ ReglaInline"""
    model = Regla
    extra = 0
    #filter_horizontal = ('niveles',)


class AmenidadAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'capacidad_maxima', 'nivel', 'requiere_reservacion',
        'costo', 'deposito'
    )
    list_filter = (
        ('actividades', admin.RelatedOnlyFieldListFilter),
        ('nivel', admin.RelatedOnlyFieldListFilter),
        'reglas__snacks', 'reglas__alcohol', 'reglas__alimentos',
        'requiere_reservacion', 'capacidad_maxima',
        'reglas__edad_minima_solo')
    search_fields = ('nombre',)
    inlines = [ReglaInline]
    filter_horizontal = ('actividades',)

    def horarios(self):
        pass

    def consumos(self):
        pass

    def edades(self):
        pass


class ReglaAdmin(admin.ModelAdmin):
    list_display = ('id', 'consumo', 'edades', 'ruido')

    # def has_module_permission(self, request, obj=None):
    #     return True

    def consumo(self, obj):
        return mark_safe(u"""
            <table>
              <tr>
                <td>Snacks permitidos</td>
                <td>{snacks}</td>
              </tr> 
              <tr>
                <td>Alimentos permitidos</td>
                <td>{alcohol}</td>
              </tr>
              <tr>
                <td>Ruido permitido</td>
                <td>{ruido}</td>
              </tr>
              <tr>
                <td>Máximo invitados</td>
                <td>{maximo_invitados}</td>
              </tr>
            </table>""".strip().format(**obj.__dict__))

    def edades(self, obj):
        return mark_safe(u"""
            <table>
              <tr>
                <td>Edad mínima (acompañado de un adulto)</td>
                <td>{edad_minima_acompanado}</td>
              </tr> 
              <tr>
                <td>Edad mínima (solo)</td>
                <td>{edad_minima_solo}</td>
              </tr>
              <tr>
                <td>Máximo invitados</td>
                <td>{maximo_invitados}</td>
              </tr>
            </table>""".strip().format(**obj.__dict__))


admin.site.register(Actividad, ActividadAdmin)
admin.site.register(Amenidad, AmenidadAdmin)
admin.site.register(Regla, ReglaAdmin)
