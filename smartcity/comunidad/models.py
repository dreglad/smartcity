# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.db import models

from localflavor.mx.models import \
    MXCURPField, MXRFCField, MXStateField, MXZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from smartcity.models import ModeloBase, EfimeroMixin



class PreferenciaContacto(ModeloBase, EfimeroMixin):
    persona = models.ForeignKey('Persona', related_name='preferencias_contacto')
    recurrencias = RecurrenceField()
    puerta = models.BooleanField(default=True)
    llamada = models.BooleanField(default=True)
    notificacion = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'preferencia de contacto'
        verbose_name_plural = u'preferencias de contacto'



class Propuesta(ModeloBase, EfimeroMixin):
    iniciado_por = models.ForeignKey(
        'Persona', related_name='iniciativas_iniciadas')
    contrapropuesta_de = models.ForeignKey(
        'self', models.SET_NULL, blank=True, null=True,
        related_name='contrapropuestas')
    contenido = models.TextField()
    a_favor = models.ManyToManyField(
        'Persona', blank=True, related_name='propuestas_a_favor')
    en_contra = models.ManyToManyField(
        'Persona', blank=True, related_name='propuestas_en_contra')
    neutrales = models.ManyToManyField(
        'Persona', blank=True, related_name='propuestas_neutrales')
    fecha_resolucion = models.DateTimeField(
        u'fecha de la resolución', null=True, blank=True)
    resolucion = models.NullBooleanField(u'resolución', null=True, blank=True)

    class Meta:
        ordering = ['-fecha_inicio']


class Comentario(ModeloBase, EfimeroMixin):
    propuesta = models.ForeignKey('Propuesta', related_name='comentarios')
    persona = models.ForeignKey('Persona', related_name='comentarios')
    contenido = models.TextField()
    respuesta_a = models.ForeignKey(
        'self', models.SET_NULL, blank=True, null=True, related_name='respuestas')

    class Meta:
        ordering = ['-fecha_inicio']

