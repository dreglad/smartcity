# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class EfimeroMixin(models.Model):
    u"""
    Para representar objetos efímeros que tienen una fecha de inicio,
    fecha de término y razón del término
    """
    fecha_inicio = models.DateField(u'fecha de inicio', db_index=True)
    fecha_termino = models.DateField(
        u'fecha de término', null=True, blank=True, db_index=True)
    razon_termino = models.CharField(
        u'razón del término', max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-fecha_inicio']


class NombrableMixin(models.Model):
    u"""Para representar objetos con nombre, descripción y slug"""
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField(u'descripción', blank=True, editable=False)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        abstract = True


class ModeloBase(models.Model):
    fecha_creacion = models.DateTimeField(
        u'fecha de creación', db_index=True, auto_now_add=True, editable=False)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, editable=False,
        related_name='%(app_label)s_%(class)s_creados')
    fecha_modificacion = models.DateTimeField(
        u'última modificación', null=True, blank=True, auto_now=True,
        editable=False)
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, editable=False,
        related_name='%(app_label)s_%(class)s_modificados')

    class Meta:
        abstract = True
