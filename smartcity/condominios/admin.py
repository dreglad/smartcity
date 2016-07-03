# -*- coding: utf-8 -*- #
from django.contrib import admin

from condominios.models import *

class DesarrolloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'domicilio',)

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_module_permission(self, request):
    #     return False


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'torre', 'nivel', 'numero', 'superficie', 'recamaras',
    )
    list_filter = (
        'torre',
        ('nivel', admin.RelatedOnlyFieldListFilter),
        'numero'
    )


class TorreAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'desarrollo')

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'identificador', 'numero', 'desarrollo')

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class LugarEstacionamientoAdmin(admin.ModelAdmin):
    list_display = ('numero_', 'nivel', 'departamento')
    list_filter = (
        ('nivel', admin.RelatedOnlyFieldListFilter),
        'departamento__torre',
        ('departamento', admin.RelatedOnlyFieldListFilter),
        
    )

    def numero_(self, obj):
        return obj.__unicode__()
    numero_.admin_order_field = 'numero'


class PropiedadAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'propietario', 'fecha_inicio', 'fecha_termino')
    list_filter = ('propietario', 'departamento', 'fecha_inicio', 'fecha_termino')


admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Desarrollo, DesarrolloAdmin)
admin.site.register(LugarEstacionamiento, LugarEstacionamientoAdmin)
admin.site.register(Nivel, NivelAdmin)
admin.site.register(Propiedad, PropiedadAdmin)
admin.site.register(Torre, TorreAdmin)
