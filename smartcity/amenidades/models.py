# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.conf import settings
from django.db import models

from smartcity.models import ModeloBase, NombrableMixin, EfimeroMixin, ProgramadoMixin


class Actividad(ModeloBase, NombrableMixin):
    DEPORTIVO = 'dep'; ENTRETENIMIENTO = 'ent'; INFANTIL = 'inf'; OTRO = 'otr'
    SERVICIO = 'ser'; FAMILIAR = 'fam'
    TIPO_CHOICES = (
        (DEPORTIVO, u'Deportivo'),
        (ENTRETENIMIENTO, u'Entretenimiento'),
        (INFANTIL, u'Infantil'),
        (FAMILIAR, u'Familiar'),
        (SERVICIO, u'Servicio'),
        (OTRO, u'Otro'),
    )
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre', 'tipo')
        verbose_name_plural = u'actividades'


class Amenidad(ModeloBase, NombrableMixin):
    actividades = models.ManyToManyField(
        'Actividad', blank=True, related_name='amenidades')
    requiere_reservacion = models.BooleanField(u'require reservación')
    costo = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    deposito = models.DecimalField(u'depósito en garantía', max_digits=10, decimal_places=2, null=True, blank=True)
    capacidad_maxima = models.PositiveIntegerField(u'capacidad máxima')
    nivel = models.ForeignKey('condominios.Nivel')

    @property
    def regla_actual(self):
        return self.reglas.latest('pk').resumen

    class Meta:
        verbose_name_plural = u'amenidades'
        ordering = ['nivel', 'nombre']


class Cartelera(ModeloBase, EfimeroMixin):
    titulo = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = u'cartelera'



class Reservacion(ModeloBase, EfimeroMixin):
    departamento = models.ForeignKey('condominios.Departamento')
    cancelado = models.BooleanField(default=False)
    amenidad = models.ForeignKey('Amenidad', related_name='reservaciones')

    class Meta:
        ordering = ['-fecha_inicio', '-fecha_termino']
        verbose_name = u'reservación'
        verbose_name_plural = u'reservaciones'


class Regla(ModeloBase, ProgramadoMixin):
    amenidad = models.ForeignKey('Amenidad', related_name='reglas')
    snacks = models.BooleanField(default=False, db_index=True)
    alimentos = models.BooleanField(default=False, db_index=True)
    alcohol = models.BooleanField(default=False, db_index=True)
    ruido = models.BooleanField(default=False, db_index=True)
    maximo_invitados = models.PositiveSmallIntegerField(
        u'máximo invitados', null=True, blank=True, db_index=True)
    edad_minima_acompanado = models.PositiveSmallIntegerField(
        u'edad mínima (acompañado)', db_index=True, null=True, blank=True,
        help_text=u'Edad mínima para usar la amenidad acompañado de un adulto')
    edad_minima_solo = models.PositiveSmallIntegerField(
        u'edad mínima (solo)', db_index=True, null=True, blank=True,
        help_text=u'Edad mínima para usar la amenidad sin compañía')

    def resumen(self):
        return u"""
            Snacks: {snacks}, Alimentos: {alimentos}, Alcohol: {alcohol},
            Ruido: {ruido}, Máx. invitados: {maximo_invitados},
            Edad mínima (acompañado): {edad_minima_acompanado},
            Edad mínima (solo): {edad_minima_solo},
            """.format(**self.__dict__)


    def __unicode__(self):
        return 'Regla para Amenidad: %s' % (self.amenidad)

