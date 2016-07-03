# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.db import models

from localflavor.mx.models import \
    MXCURPField, MXRFCField, MXStateField, MXZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from smartcity.models import ModeloBase, EfimeroMixin



class ContribuyenteMixin(models.Model):
    rfc = MXRFCField(
        u'RFC', blank=True, help_text=u'Registro Federal de Contribuyentes')
    domicilio_fiscal = models.ForeignKey('Domicilio', blank=True, null=True)
    razon_social = models.CharField(
        u'razón social', max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class Domicilio(ModeloBase):
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(u'número exterior', max_length=32)
    numero_interior = models.CharField(
        u'número interior', max_length=32, blank=True)
    colonia = models.CharField(max_length=128, blank=True)
    delegacion = models.CharField(u'delegación o municipio', max_length=64, blank=True)
    codigo_postal = MXZipCodeField(u'código postal', help_text='aa', editable=True)
    estado = MXStateField()
    pais = models.CharField(default=u'México', max_length=64)

    @property
    def estado_display(self):
        return self.get_estado_display()

    @property
    def numero_completo(self):
        if self.numero_interior:
            return u'%s Int. %s' % (self.numero_exterior, self.numero_interior)
        else:
            return self.numero_exterior
    
    def __unicode__(self):
        return u'{calle} {numero_completo}, C.P. {codigo_postal}' \
                .format(numero_completo=self.numero_completo, **self.__dict__)

    class Meta:
        ordering = ('calle', 'numero_exterior', 'numero_interior')


class Organizacion(ModeloBase, ContribuyenteMixin):
    nombre = models.CharField(max_length=255)
    domicilio = models.ForeignKey(
        'Domicilio', blank=True, null=True, related_name='organizaciones')


class Persona(ModeloBase, ContribuyenteMixin):
    MASCULINO = 'M'; FEMENIMO = 'F'
    GENERO_CHOICES = ((MASCULINO, 'Masculino'), (FEMENIMO, 'Femenino'))
    A = 'A'; B = 'B'; AB = 'AB'; O = 'O'
    GRUPO_SANGUINEO_CHOICES = zip((A, B, AB, O), (A, B, AB, O))

    nombre = models.CharField(u'nombre(s) de pila', max_length=255)
    domicilio = models.ForeignKey(
        u'Domicilio', blank=True, null=True, related_name='personas')
    responsables = models.ManyToManyField(u'self', related_name='menores')
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255, blank=True)
    genero = models.CharField(u'género', max_length=1, choices=GENERO_CHOICES)
    curp = MXCURPField(
        u'CURP', blank=True, help_text='Clave Única de Registro de Publación')
    fecha_nacimiento = models.DateField(u'fecha de nacimiento')
    lugar_nacimiento = models.CharField(
        u'lugar de nacimiento', max_length=255, blank=True)
    fecha_fallecimiento = models.DateField(
        u'fecha de fallecimiento', blank=True, null=True,
        help_text='Q. E. P. D.')
    lugar_fallecimiento = models.CharField(
        u'lugar de fallecimiento', max_length=255, blank=True)

    foto = models.FileField(blank=True)

    # médico
    grupo_sanguineo = models.CharField(
        u'grupo sanguíneo', blank=True, max_length=2, choices=GRUPO_SANGUINEO_CHOICES)
    rh_sanguineo = models.BooleanField(u'RH Sanguíneo', blank=True)
    alergias = models.TextField(blank=True)
    discapacidades = models.ManyToManyField(
        'Discapacidad', blank=True, related_name='personas')

    def __unicode__(self):
        return (
            u'%s %s %s' % (
                self.nombre, self.apellido_paterno,
                self.apellido_materno)
            ).strip()

    @property
    def edad(self):
        hoy, nacimiento = date.today(), self.fecha_nacimiento
        return hoy.year - nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month,
                                    self.fecha_nacimiento.day))

    def adulto(self):
        return self.edad >= 18

    class Meta:
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']



class Discapacidad(ModeloBase, EfimeroMixin):
    AUDITIVO = 'au'; COGNITIVO = 'co'; MOTRIZ = 'mo'; VISUAL = 'vi'; OTRO = 'ot'
    TIPO_CHOICES = (
        (AUDITIVO, u'Auditivo'),
        (COGNITIVO, u'Cognitivo'),
        (MOTRIZ, u'Motriz'),
        (VISUAL, u'Visual'),
        (OTRO, u'Otro'),
    )
    LEVE = 0; MEDIA = 1; GRAVE = 2
    SEVERIDAD_CHOICES = (
        (0, u'leve/temporal'),
        (1, u'media/parcial'),
        (2, u'grave/total'),
    )
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    severidad = models.PositiveSmallIntegerField()
    observaciones = models.TextField(
        blank=True, help_text=(u'Especifique cualquier información adicional, ' 
                               u'por ejemplo atenciones especiales requeridas'))


# class TrabajadorMixin(models.Model):
#     seguro_social = MXSocialSecurityNumberField()

# class Visita(ModeloBase, EfimeroMixin):
#     persona = models.ForeignKey('Persona')
#     departamento = models.ForeignKey('Departamento')
#     autorizado_por = persona = models.ForeignKey('Persona')


# class SueldoCargo(ModeloBase, EfimeroMixin):
#     cargo = models.ForeignKey('Cargo', models.CASCADE)
#     importe = models.FloatField()
#     periodo = models.

# class Cargo(ModeloBase, EfimeroMixin):
#     TIPO = ('empleado', 'electo', 'voluntario')
#     persona = models.ForeignKey('Persona')

# class Condomino(ModeloBase, EfimeroMixin):
#     persona = models.ForeignKey('Persona', verbose_name=u'propiedades')
#     departamento = models.ForeignKey('condominios.Departamento', related_name='propiedades')

#     class Meta():
#         ordering = ['departamento']
#         verbose_name_plural = u'propiedad'
