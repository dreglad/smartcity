# -*- coding: utf-8 -*- #}
from __future__ import unicode_literals
from datetime import date

from dateutil import relativedelta
from django.conf import settings
from django.db import models
from recurrence.fields import RecurrenceField
from django.forms.models import model_to_dict

from smartcity.models import ModeloBase, NombrableMixin, EfimeroMixin


class MontoMixin(object):
    """
    Mixin that handles monto_ndto, IVA and monto_bruto fields on save()

    """
    def set_monto_fields(self):
        if self.monto_neto and not self.monto_bruto:
            if self.iva:
                self.monto_bruto = \
                    self.monto_neto * (self.iva / Decimal(100.0) + 1)
            else:
                self.monto_bruto = self.monto_neto

        if self.monto_bruto and not self.monto_neto:
            if self.vat:
                self.monto_neto = \
                    Decimal(1.0) / (self.iva / Decimal(100.0) + 1) \
                    * self.monto_bruto
            else:
                self.monto_neto = self.monto_bruto

    def set_valor_fields(self, tipo_field_name):
        multiplier = 1
        tipo_ = getattr(self, tipo_field_name)
        if tipo_ == Transaccion.DEPOSITO:
            multiplier = -1
        self.monto_neto = self.monto_neto * multiplier
        self.monto_bruto = self.monto_bruto * multiplier


class Servicio(ModeloBase, NombrableMixin):
    SEGURIDAD = 'seg'
    ADMINISTRACION = 'adm'
    MATENIMIENTO = 'man'
    TIPO_CHOICES = (
        (ADMINISTRACION, u'Administración'),
        (SEGURIDAD, u'Seguridad'),
        (MATENIMIENTO, u'Mantenimiento'),
    )
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)


class Cuota(ModeloBase, NombrableMixin, EfimeroMixin):
    monto = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    recurrencia = RecurrenceField()
    tolerancia = models.DurationField(blank=True, null=True)
    recargos = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __unicode__(self):
        return u'{0} (${1:,.2f})'.format(self.nombre, self.monto)
    class Meta:
        pass


class PagoCuota(ModeloBase, NombrableMixin, EfimeroMixin):
    cuota = models.ForeignKey('Cuota', related_name='pagos')
    monto = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    cuenta_pago = models.ForeignKey(
        'CuentaBancaria', related_name='pagos_de_cuotas')
    class Meta:
        verbose_name = u'pago de cuota'
        verbose_name_plural = u'pagos de cuotas'


class Licitacion(ModeloBase, NombrableMixin):
    servicio = models.ForeignKey('Servicio')
    # documentos = models.ManyToManyField('humanos.Documentos')
    class Meta:
        verbose_name = u'licitación'
        verbose_name_plural = u'licitaciones'


# class Transaccion(ModeloBase):
#     pass



class Factura(ModeloBase):
    recibo = models.ForeignKey('Recibo', )




class Contrato(ModeloBase, EfimeroMixin):
    proveedor = models.ForeignKey('humanos.Persona', related_name='contratos')
    servicio = models.ForeignKey('Servicio', related_name='contratos')
    recurrencias = RecurrenceField()

    class Meta:
        ordering = ['-fecha_termino', 'fecha_inicio']


class EvaluacionServicio(ModeloBase):
    persona = models.ForeignKey(
        'humanos.Persona', related_name='evaluaciones_servicio')
    contrato = models.ForeignKey(
        'Contrato', related_name='evaluaciones_servicio')

    class Meta:
        verbose_name = u'evaluación de servicio'
        verbose_name_plural = u'evaluaciones de servicio'


class Cuenta(models.Model):
    alias = models.CharField(max_length=128)

    # divisa = models.ForeignKey(
    #     'currency_history.Currency', related_name='accounts')

    saldo_inicial = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    saldo_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __unicode__(self):
        return self.alias

    def get_saldo(self, mes=None):
        """Returns the balance up until now or until the provided mes."""
        mes = mes or date(date.today().year, date.today().month, 1)
        next_mes = mes + relativedelta.relativedelta(months=1)
        saldo_acumulado = self.transacciones.filter(
            parent__isnull=True, fecha__lt=next_mes,
        ).aggregate(models.Sum('valor_bruto'))['valor_bruto__sum'] or 0
        return self.saldo_inicial + saldo_acumulado



class Banco(ModeloBase):
    clave = models.CharField(max_length=64)
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.clave

    class Meta:
        ordering = ['clave', 'nombre']


class CuentaBancaria(ModeloBase, EfimeroMixin, NombrableMixin):
    beneficiario = models.ForeignKey(
        'humanos.Persona', related_name='cuentas_bancarias')
    banco = models.ForeignKey('Banco', related_name='cuentas_bancarias')
    numero = models.CharField(u'número', max_length=64, blank=True, null=True)
    clabe = models.CharField(
        u'CLABE', help_text=u'Clave Bancaria Estandarizada', null=True,
        blank=True, max_length=18)
    referencias = models.TextField(blank=True)

    def __unicode__(self):
        return u'{nombre}, {banco} #{numero} a nombre de {beneficiario}'.format(
            nombre=self.nombre, banco=self.banco, numero=self.numero,
            beneficiario=self.beneficiario)

    class Meta:
        verbose_name = u'cuenta bancaria'
        verbose_name_plural = u'cuentas bancarias'


class CuentaPersonal(ModeloBase, EfimeroMixin):
    beneficiario = models.ForeignKey('humanos.Persona')

    class Meta:
        verbose_name = u'cuenta bancaria personal'
        verbose_name_plural = u'cuentas bancarias personales'


class CuentaEmpresarial(ModeloBase, EfimeroMixin):
    beneficiario = models.ForeignKey('humanos.Organizacion')

    class Meta:
        verbose_name = u'cuenta bancaria empresarial'
        verbose_name_plural = u'cuentas bancarias empresariales'


class Proveedor(ModeloBase, EfimeroMixin):
    organizacion = models.ForeignKey('humanos.Organizacion')

    class Meta:
        verbose_name_plural = 'proveedores'






class ReciboManager(models.Manager):
    """Custom manager for the ``Invoice`` model."""
    def get_without_pdf(self):
        qs = Recibo.objects.filter(pdf='')
        qs = qs.prefetch_related('transactions', )
        return qs



class Recibo(MontoMixin, models.Model):
    DEPOSITO = 'd'
    RETIRO = 'r'

    TIPO_CHOICES = (
        (DEPOSITO, u'Depósito'),
        (RETIRO, u'Retiro'),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    fecha = models.DateField()
    fecha_pago = models.DateField(blank=True, null=True)

    numero = models.CharField(u'número', max_length=256, blank=True)
    descripcion = models.TextField(u'descripción', blank=True)

    monto_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    monto_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    iva = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    valor_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    recibo_pdf = models.FileField(upload_to='recibos', blank=True, null=True)
    factura_pdf = models.FileField(upload_to='rrecibod', blank=True, null=True)
    factura_xml = models.FileField(upload_to='facturas/', blank=True, null=True)
    factura_cbd = models.FileField(upload_to='facturas/', blank=True, null=True)

    objects = ReciboManager()

    class Meta:
        ordering = ['-fecha', ]

    def __unicode__(self):
        if self.numero:
            return self.numero
        return '{0} - {1}'.format(self.fecha,
                                  self.get_tipo_display())

    def save(self, *args, **kwargs):
        self.set_monto_fields()
        self.set_valor_fields('tipo')
        return super(Recibo, self).save(*args, **kwargs)

    @property
    def saldo(self):
        if not self.transacciones.all():
            return 0 - self.monto_neto

        total = 0
        # Convert amounts
        
        # Get transacciones for each currency
        transacciones = self.transacciones.all()

        # if divisa == self.divisa:
        #     rate = 1
        # else:
        #     rate = Decimal(CurrencyRateHistory.objects.filter(
        #         rate__from_currency=divisa,
        #         rate__to_currency=self.divisa,
        #     )[0].value)
        if transacciones:
            rate = 1
            total += rate * transacciones.aggregate(
            models.Sum('monto_neto'))['monto_neto__sum']
        return total - self.monto_neto




class TransaccionManager(models.Manager):
    """Manager for the ``Transaccion`` model."""
    def get_totals_by_payee(self, account, start_date=None, end_date=None):
        """
        Returns transaccion totals grouped by Payee.
        """
        qs = Transaccion.objects.filter(account=account, parent__isnull=True)
        qs = qs.values('payee').annotate(models.Sum('valor_bruto'))
        qs = qs.order_by('payee__name')
        return qs

    def get_without_invoice(self):
        """
        Returns transacciones that don't have an invoice.
        We filter out transacciones that have children, because those
        transacciones never have invoices - their children are the ones that
        would each have one invoice.
        """
        qs = Transaccion.objects.filter(
            children__isnull=True, invoice__isnull=True)
        return qs



class ReciboMantenimiento(Recibo):
    recurrencias = RecurrenceField()


class Transaccion(MontoMixin, models.Model):
    TRANSACTION_TYPES = {
        'withdrawal': 'w',
        'deposit': 'd',
    }

    TRANSACTION_TYPE_CHOICES = [
        (TRANSACTION_TYPES['withdrawal'], 'withdrawal'),
        (TRANSACTION_TYPES['deposit'], 'deposit'),
    ]

    cuenta = models.ForeignKey(Cuenta, related_name='transacciones')

    parent = models.ForeignKey(
        'self', models.SET_NULL, related_name='children', blank=True, null=True)

    tipo = models.CharField(
        max_length=1,
        choices=TRANSACTION_TYPE_CHOICES,
    )

    fecha = models.DateField()

    decripcion = models.TextField(blank=True)

    numero = models.CharField(max_length=256, blank=True)

    recibo = models.ForeignKey(
        'Recibo', blank=True, null=True, related_name='transacciones')

    beneficiario = models.ForeignKey('humanos.Persona', related_name='transacciones')

    # concepto = models.ForeignKey('Category', related_name='transacciones')

    # divisa = models.ForeignKey(
    #     'currency_history.Currency', related_name='transacciones',)

    monto_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    iva = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    monto_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0,blank=True,)
    valor_neto = models.DecimalField(max_digits=10,decimal_places=2,default=0,)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = TransaccionManager()

    class Meta:
        ordering = ['-fecha', ]

    def __unicode__(self):
        if self.numero:
            return self.numero
        if self.invoice and self.invoice.numero:
            return self.invoice.numero
        return '{0} - {1}'.format(self.payee, self.category)

    def get_decripcion(self):
        if self.decripcion:
            return self.decripcion
        if self.invoice and self.invoice.decripcion:
            return self.invoice.decripcion
        decripcion = ''
        for child in self.children.all():
            if child.decripcion:
                decripcion += u'{0},\n'.format(child.decripcion)
            elif child.invoice and child.invoice.decripcion:
                decripcion += u'{0},\n'.format(child.invoice.decripcion)
        return decripcion or u'n/a'

    def get_invoices(self):
        if self.children.all():
            return [child.invoice for child in self.children.all()]
        return [self.invoice, ]

    def save(self, *args, **kwargs):
        self.set_amount_fields()
        self.set_value_fields('tipo')
        return super(Transaccion, self).save(*args, **kwargs)

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

