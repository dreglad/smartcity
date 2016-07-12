# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.db import models

from localflavor.mx.models import \
    MXCURPField, MXRFCField, MXStateField, MXZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from smartcity.models import ModeloBase, EfimeroMixin, NomradoMixin



class TipoDispositivo(ModeloBase, NomradoMixin):
    nivel = models.ForeignKey('condominios.Nivel')

    class Meta:
        verbose_name = u'tipo de dispositivo'
        verbose_name_plural = u'Tipos de dispositvo'


class Dispositivo(ModeloBase, EfimeroMixin)
    identificador = models.CharField(max_length=32)
    nivel = models.ForeignKey('Nivel', related_name='sensores')
    ultimo_servicio = models.DateTimeField(
        u'fecha de último servicio', blank=True, null=True)

    class Meta:
