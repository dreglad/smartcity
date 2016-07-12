# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.db import models

from localflavor.mx.models import \
    MXCURPField, MXRFCField, MXStateField, MXZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from smartcity.models import ModeloBase, EfimeroMixin


# class Accion(ModeloBase, NombrableMixin):


# class Voto(ModeloBase, EfimeroMixin):
#     iniciativa = models.ForeignKey('Iniciativa')
#     persona = models.ForeignKey('Persona')
#     resolucion 



class Reporte(ModeloBase, EfimeroMixin):
    iniciado_por = models.ForeignKey('humanos.Persona', related_name='reportes_iniciados')
    resolucion = models.TextField(u'resolución', blank=True)
    class Meta:
        ordering = ['-fecha_inicio', '-fecha_termino']



class Visita(ModeloBase, EfimeroMixin):
    persona = models.ForeignKey('humanos.Persona', related_name='visitas')
    departamento = models.ForeignKey(
        'condominios.Departamento', related_name='visitas')

    def __unicode__(self):
        txt = u'{0} visita al {1} el {2}'.format(
            self.persona, self.departamento, self.fecha_creacion)
        if self.fecha_termino:
            txt += u' y sale el {0}'.format(self.fecha_termino)
        return txt

    class Meta:
        ordering = ['-fecha_creacion', '-fecha_termino']


# class ReporteVehiculo(Reporte)
