# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.conf import settings
from django.db import models

from smartcity.models import ModeloBase, NombrableMixin, EfimeroMixin

class Banco(models.Model):
    clave = models.CharField(max_length=32)
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.clave

    class Meta:
        ordering = ['clave']


class Transaccion():
    pass


class Ingreso():
    pass


class Egreso():
    pass


class CuentaBancaria(ModeloBase, EfimeroMixin):
    BANCOS_MEXICANOS = (
        ('BMX', 'Banamex',),
        ('BVA', 'BBVA Bancomer'),
        ('SAN', 'Santander'),
        ('HSB', 'HSBC'),
        ('BNT', 'Banorte'),
        ('IXE', 'Ixe banco'),
    )
    banco = models.CharField(max_length=64, choices=BANCOS_MEXICANOS)
    beneficiario = models.ForeignKey('humanos.Persona')

    class Meta:
        verbose_name = u'cuenta bancaria'
        verbose_name_plural = u'cuentas bancarias'


# class CuentaCheques(CuentaBancaria):
#     clabe = MXCLABEField(u'CLABE', help_text=u'Clave Bancaria Estandarizada')

#     class Meta:
#         verbose_name = u'cuenta de cheques'
#         verbose_name_plural = u'cuentas de cheques'


# class CuentaAhorros(ModeloBase):
#     numero_cuenta = models.CharField(u)

#     class Meta:
#         verbose_name = u'cuenta de ahorros'
#         verbose_name_plural = u'cuentas de ahorros'





# class Discapacidad(ModeloBase, EfimeroMixin):
#     TIPO = Choices(
#         ('a', u'Auditiva'),
#         ('c', u'Cognitiva'),
#         ('m', u'Motriz'),
#         ('v', u'Visual')
#     )
#     SEVERIDAD = Choices(
#         ('p', u'parcial/leve'),
#         ('l', u'total/grave'),
#     )
#     ORIGEN = Choices(
#         ('a', u'Adquirido'),
#         ('c', u'Congénito'),
#     )
#     diagnostico = models.CharField(u'diagnóstico', max_length=255 blank=True,
#                                    help_text=u'Nombre del diagneostico médito')

#     def fecha_inicial_display(self):
#         return u'fecha del diagnóstico'


# class Documento(ModeloBase):
#     archivo = models.ModelField

# class Video(Documento, NombrableMixin):
#     thumbnail
#     sprites
#     hls

# class Imagen(Documento):
#     pass



# class Vehiculo(ModeloBase):
#     placas
#     responsable
#     marca
#     submarca
#     version
#     modelo
#     color

#     class Meta:
#         verbose_name = u'vehículo'
#         verbose_name_plural = u'vehículos'


# class Reporte(ModeloBase)

# class ReporteVehiculo(Reporte)


# class Estacionada(ModeloBase, EfimeroMixin):
#     lugar = models.ForeignKey('LugarEstacionamiento', models.SET_NULL)
#     vehiculo = models.ForeignKey(
#         'LugarEstacionamiento', models.SET_NULL, verbose_name=u'vehículo')


# class LineaTelefonica(ModeloBase, EfimeroMixin):
#     numero = PhoneNumberField(u'número')

#     class Meta:
#         verbose_name = u'línea telefónica'
#         verbose_name = u'líneas telefónicas'


# class TelefonoFijo(LineaTelefonica):
#     extension = models.PositiveIntegerField(u'extensión', null=True)

#     class Meta:
#         verbose_name = u'teléfono fijo'
#         verbose_name_plural = u'teléfonos fijos'


# class LineaCelular(LineaTelefonica):
#     COMPANIA = ('Telcel', 'Movistar', 'Iusacell', 'AT&T', 'Otro')
#     compania = models.CharField(u'compañía', choices=COMPANIA, blank=True)

#     class Meta:
#         verbose_name = u'línea celular'
#         verbose_name_plural = u'líneas celulares'


# class CelularDispositivoMovil(BaseModel, EfimeroMixin):
#     celular =
#     dispositivo_movil =

#     class Meta:
#         verbose_name = u'celular en dispositivo móvil'
#         verbose_name_plural = u'celulares en dispositivos móviles'


# class DispositivoMovil(BaseModel):
#     SISTEMA_OPERATIVO = ('Telcel', 'Movistar', 'Iusacell', 'AT&T', 'Otro')
#     sistema_operativo = models.CharField(max_length=32, blank=True)
#     modelo = models.CharField(max_length=255)

#     class Meta:
#         verbose_name = u'dispositivo móvil'
#         verbose_name_plural = u'dispositivos móviles'


# class Smartphone(DispositivoMovil):
#     dispositivo_movil = models.ForeignKey('DispositivoMovil')
#     lineas_celulares = models.ManyToManyField(
#         'Celular', models.SET_NULL, through='ChipEnDispositivoMovil',
#         related_name=u'smartphones'

#     def get_linea_celular(self):
#         u"""Devuelve el celular actual"""
#         return self.lineas_celulares.actual()

#     class Meta:
#         verbose_name = u'número de celular'
#         verbose_name = u'números de celular'




#     Futuro
#        - Antónimo de "Divide y vencerás" Infraestructura
#     """
#     clasificacion = models.CharField(max_length=8, choices=CLASIFICACION)
#     amenidades = model.ManyToManyField(
#        'Amenidad', blank=True, help_text=(u'Amenidad(es) en las cuales se puede'
#                                           u' practivar esta actividad'))



# class Evento(ModeloBase, NombrableMixin, EfimeroMixin):
#     pass


# class Cartelera():
#     pass


# class ResponsableArea(ModeloBase, EfimeroMixin):
#     persona = models.ForeignKey('Persona')
#     area = models.ForeignKey('Area')

#     class Meta:


# class ProgramadoMixin(models.Model):
#     #recurrencias = recurrence.fields.RecurrenceField()
#     lunes_lunes = models.TimeField(blank=True, null=True, db_index=True)
#     lunes_martes = models.TimeField(blank=True, null=True, db_index=True)
#     lunes_miercoles = models.TimeField(u'miércoles', blank=True, null=True, db_index=True)
#     lunes_jueves = models.TimeField(blank=True, null=True, db_index=True)
#     lunes_viernes = models.TimeField(blank=True, null=True, db_index=True)
#     lunes_sabado = models.TimeField(u'sábado', blank=True, null=True, db_index=True)
#     lunes_domingo = models.TimeField(blank=True, null=True, db_index=True)

#     class Meta:
#         abstract = True


# class Actividad(ModeloBase, NombrableMixin):
#     DEPORTIVO = 'dep'; ENTRETENIMIENTO = 'ent'; INFANTIL = 'inf'; OTRO = 'otr'
#     SERVICIO = 'ser'; FAMILIAR = 'fam'
#     TIPO_CHOICES = (
#         (DEPORTIVO, u'Deportivo'),
#         (ENTRETENIMIENTO, u'Entretenimiento'),
#         (INFANTIL, u'Infantil'),
#         (FAMILIAR, u'Familiar'),
#         (SERVICIO, u'Servicio'),
#         (OTRO, u'Otro'),
#     )
#     tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)

#     def __unicode__(self):
#         return self.nombre

#     class Meta:
#         ordering = ('nombre', 'tipo')
#         verbose_name_plural = u'actividades'


# class Amenidad(ModeloBase, NombrableMixin):
#     actividades = models.ManyToManyField(
#         'Actividad', blank=True, related_name='amenidades')
#     requiere_reservacion = models.BooleanField(u'require reservación')
#     costo = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
#     deposito = models.DecimalField(u'depósito en garantía', max_digits=10, decimal_places=2, null=True, blank=True)
#     capacidad_maxima = models.PositiveIntegerField(u'capacidad máxima')
#     nivel = models.ForeignKey('Nivel')

#     @property
#     def regla_actual(self):
#         return self.reglas.latest('pk').resumen

#     class Meta:
#         verbose_name_plural = u'amenidades'
#         ordering = ['nivel', 'nombre']


# class Regla(ModeloBase, ProgramadoMixin):
#     amenidad = models.ForeignKey('Amenidad', related_name='reglas')
#     snacks = models.BooleanField(default=False, db_index=True)
#     alimentos = models.BooleanField(default=False, db_index=True)
#     alcohol = models.BooleanField(default=False, db_index=True)
#     ruido = models.BooleanField(default=False, db_index=True)
#     maximo_invitados = models.PositiveSmallIntegerField(
#         u'máximo invitados', null=True, blank=True, db_index=True)
#     edad_minima_acompanado = models.PositiveSmallIntegerField(
#         u'edad mínima (acompañado)', db_index=True, null=True, blank=True,
#         help_text=u'Edad mínima para usar la amenidad acompañado de un adulto')
#     edad_minima_solo = models.PositiveSmallIntegerField(
#         u'edad mínima (solo)', db_index=True, null=True, blank=True,
#         help_text=u'Edad mínima para usar la amenidad sin compañía')

#     def resumen(self):
#         return u"""
#             Snacks: {snacks}, Alimentos: {alimentos}, Alcohol: {alcohol},
#             Ruido: {ruido}, Máx. invitados: {maximo_invitados},
#             Edad mínima (acompañado): {edad_minima_acompanado},
#             Edad mínima (solo): {edad_minima_solo},
#             """.format(**self.__dict__)


#     def __unicode__(self):
#         return 'Regla para Amenidad: %s' % (self.amenidad)

