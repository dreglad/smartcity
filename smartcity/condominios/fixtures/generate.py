# -*- coding: utf-8 -*- #}
from condominios.models import Departamento, Desarrollo, Nivel, Torre
from humanos.models import Domicilio


DESARROLLO = {
    'nombre': u'City Towers Grand',
    'domicilio': {
        'calle': u'Av. Popocatépetl',
        'numero_exterior': u'474',
        'colonia': u'Xoco',
        'delegacion': u'Benito Juárez',
        'codigo_postal': u'03330',
        'estado': u'DIF',
        'pais': u'México',
    },
    'torres': ('A', 'B', 'C', 'D', 'E', 'F'),
    'niveles': (
        (-5, -1, 'S{numero}', u'Sótano {numero}'),
        (0, 0, 'PB', u'Planta Baja'),
        (1, 21, '{numero}', u'Piso {numero}'),
        (22, 22, 'RG', 'Roof Garden'),
    ),
    'niveles_habitables': range(1, 22),
    'departamentos_por_nivel': 4
}

def generate_desarrollo():
    Desarrollo.objects.create(
        domicilio=Domicilio.objects.create(**DESARROLLO['domicilio']),
        nombre=DESARROLLO['nombre'])

def generate_torres():
    desarrollo = Desarrollo.objects.get(nombre=DESARROLLO['nombre'])
    for torre in DESARROLLO['torres']:
        Torre.objects.create(desarrollo=desarrollo, identificador=torre)

def generate_niveles():
    desarrollo = Desarrollo.objects.get(nombre=DESARROLLO['nombre'])
    for nivel in DESARROLLO['niveles']:
        for num in range(nivel[0], nivel[1]+1):
            Nivel.objects.create(
                desarrollo=desarrollo, numero=num,
                identificador=nivel[2].format(numero=abs(num)),
                nombre=nivel[3].format(numero=abs(num))
                )

def generate_departamentos():
    torres = Torre.objects.filter(desarrollo__nombre=DESARROLLO['nombre'])
    for torre in torres:
        for nivel in torre.desarrollo.niveles.filter(
                numero__in=DESARROLLO['niveles_habitables']):
            for numero in range(1, DESARROLLO['departamentos_por_nivel']+1):
                try:
                    Departamento.objects.create(
                        torre=torre, nivel=nivel, numero=numero)
                except Departamento.ValidationError:
                    pass

def load_fixtures():
    generate_desarrollo()
    generate_torres()
    generate_niveles()
    generate_departamentos()