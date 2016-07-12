# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date

from django.db import models

from localflavor.mx.models import \
    MXCURPField, MXRFCField, MXStateField, MXZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from smartcity.models import ModeloBase, EfimeroMixin
from smartcity.admin import SmartCityModelAdmin



class Vehiculo(ModeloBase):
    placas = models.CharField(max_length=8)
    responsable = models.ForeignKey('humanos.Persona', related_name='vehiculos')
    marca = models.CharField(max_length=64, blank=True)
    submarca = models.CharField(max_length=64, blank=True)
    modelo = models.PositiveSmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return u'{marca} {color} placas {placas}'.format(**self.__dict__)

    class Meta:
        verbose_name = u'vehículo'
        verbose_name_plural = u'vehículos'



class LugarEstacionamientoQuerySet(models.QuerySet):

    def lugares_disponibles(self):
        return self.filter(vehiculos_estacionados__fecha_termino__isnull=True)

    def lugares_ocupados(self):
        return self.filter(vehiculos_estacionados__fecha_termino__isnull=False)



class LugarEstacionamiento(ModeloBase):
    """Representa un lugar de estacionamiento"""
    numero = models.PositiveIntegerField()
    nivel = models.ForeignKey(
        'condominios.Nivel', related_name='lugares_estacionamiento')
    departamento = models.ForeignKey(
        'condominios.Departamento', blank=True, null=True,
        related_name='lugares_estacionamiento')
    estorba_con = models.ManyToManyField('self', blank=True)

    # objects = LugarEstacionamientoQuerySet.as_manager()

    def __unicode__(self):
        return u'%03d' % self.numero

    def es_lugar_visita(self):
        return self.departamento is None

    class Meta:
        ordering = ['numero']
        verbose_name = u'lugar de estacionamieno'
        verbose_name_plural = u'lugares de estacionamieno'


class VehiculoEstacionado(ModeloBase, EfimeroMixin):
    vehiculo = models.ForeignKey('Vehiculo', related_name='estacionadas')
    lugar = models.ForeignKey(
        'LugarEstacionamiento', related_name='vehiculos_estacionados')

    def __unicode__(self):
        txt = (u'{vehiculo.marca} {vehiculo.color} estacionado en lugar '
               u' {lugar} desde el {fecha_inicio}').format(
                    vehiculo=self.vehiculo, lugar=self.lugar,
                    fecha_inicio=self.fecha_inicio)
        if self.fecha_termino:
            txt += u' hasta el {fecha_termino}'.format(**self.__dict__)
        return txt

    class Meta:
        verbose_name = u'vehículo estacionado'
        verbose_name_plural = u'vehículos estacionados'

