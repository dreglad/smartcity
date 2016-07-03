# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from django.db import models

from smartcity.models import ModeloBase, NombrableMixin, EfimeroMixin


class Desarrollo(ModeloBase):
    nombre = models.CharField(max_length=128)
    domicilio = models.ForeignKey('humanos.Domicilio')
    #constructor = models.ForeignKey('Organizacion')
    #cuotas = models.ManyToManyField('Cuota')

    def __unicode__(self):
        return self.nombre


class Torre(ModeloBase):
    desarrollo = models.ForeignKey('Desarrollo', related_name='torres')
    identificador = models.CharField(max_length=8)

    def __unicode__(self):
        return self.identificador

    class Meta:
        ordering = ['desarrollo', 'identificador']


class Departamento(ModeloBase):
    torre = models.ForeignKey('Torre', related_name='departamentos')
    nivel = models.ForeignKey('Nivel', related_name='departamentos')
    numero = models.PositiveSmallIntegerField(u'número')
    superficie = models.FloatField(
        blank=True, null=True,
        help_text=u'superficie en metros cuadrados')
    recamaras = models.PositiveSmallIntegerField(
        u'recámaras', null=True, blank=True,
        choices=((1, u'1'), (2, u'2'), (3, u'3')))

    def __unicode__(self):
        return '%s-%s%02d' % (self.torre, self.nivel.identificador, self.numero)

    class Meta:
        ordering = ['torre', 'nivel', 'numero']
        unique_together = (('torre', 'nivel', 'numero',),)
        index_together = (('torre', 'nivel', 'numero',),)


# class Visita(ModeloBase, EfimeroMixin):
#     persona = models.ForeignKey('Persona')
#     departamento = models.ForeignKey('Departamento')
#     autorizado_por = persona = models.ForeignKey('Persona')



class LugarEstacionamiento(ModeloBase):
    """Representa un lugar de estacionamiento"""
    numero = models.PositiveIntegerField()
    nivel = models.ForeignKey('Nivel', related_name='lugares_estacionamiento')
    departamento = models.ForeignKey(
        'Departamento', blank=True, null=True,
        related_name='lugares_estacionamiento')
    estorba_con = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return u'%03d' % self.numero

    def es_lugar_visita(self):
        return self.departamento is None

    class Meta:
        ordering = ['numero']
        verbose_name = u'lugar de estacionamieno'
        verbose_name_plural = u'lugares de estacionamieno'



class Nivel(ModeloBase):
    desarrollo = models.ForeignKey('Desarrollo', related_name='niveles')
    identificador = models.CharField(
        max_length=8, help_text=(
            (u'Abreviación que típicamente coincide con los rótulos de los '
            u'botones del elevador. Por ejemplo: PB, S1, RG, 1, 2, 3, ...'))
    )
    nombre = models.CharField(
        max_length=64, help_text=(
            u'Por ejemplo: Piso 4, Planta Baja, Sótano 3, Roof Garden, Piso 21')
    )
    numero = models.SmallIntegerField(u'número',)
    ## no necesario hay_departamentos = models.BooleanField(help_text=u'¿En este nivel hay departamentos habitables?')
    #hay_amenidades = models.BooleanField(help_text=u'¿En este nivel hay amenidades?')
    #hay_estacionamientos = models.BooleanField(default=False, help_text=u'¿En este nivel hay lugares de estacionamiento?')

    def __unicode__(self):
        return u'%s (%s)' % (self.identificador, self.nombre)

    class Meta:
        ordering = ['numero']
        verbose_name_plural = u'niveles'


class Propiedad(ModeloBase, EfimeroMixin):
    propietario = models.ForeignKey('humanos.Persona', verbose_name=u'propiedades')
    departamento = models.ForeignKey('Departamento', related_name='propiedades')

    class Meta():
        ordering = ['departamento']
        verbose_name_plural = u'propiedad'

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





# class Area(ModeloBase, NombrableMixin):
#     niveles = models.ManyToManyField('Nivel')


# CLASIFICACION = Choices(
#     'aa', u'Dirigido a niños',
#     'a', u'Dirigido a toda la familia',
#     'b', u'Dirigido a adolescentes y adultos',
#     'c', u'Dirigido a adultos',
# )

# class TipoActividad(ModeloBase, NombrableMixin):
#     """
#     Define un tipo de actividad:
#         deportiva, recreativa, familiar, didáctica, civil, vecinal
#     """
#     clasificacion = models.CharField(choices=CLASIFICACION)


# class Actividad():
#    """
#    natacion
#    golf
#    yoga
#    acondicionamiento físico
#    boliche
#    cine
#    maquinitas
#    yacuzzi
#    vapor
#    sauna
#    regaderas
#    billar
#    televisión
#    cine al aire libre
#    paddle
#    caminar
#    Parrillada
#    Reuniones de trabajo
#    Eventos sociales
#    Estudiar
#    Jugar
#    chapoteadero
#    estética
#    Comer
#    Comprar

#    Reglas de conviencia
#       - Vigilancia

#       -

#      - Democracia

#     Pagos
#        - Pagos recurrentes
#        - Paypal


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

