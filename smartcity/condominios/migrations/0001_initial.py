# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 04:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('humanos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('numero', models.PositiveSmallIntegerField(verbose_name='n\xfamero')),
                ('superficie', models.FloatField(blank=True, help_text='superficie en metros cuadrados', null=True)),
                ('recamaras', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3')], null=True, verbose_name='rec\xe1maras')),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_departamento_creados', to=settings.AUTH_USER_MODEL)),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_departamento_modificados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['torre', 'nivel', 'numero'],
            },
        ),
        migrations.CreateModel(
            name='Desarrollo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('nombre', models.CharField(max_length=128)),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_desarrollo_creados', to=settings.AUTH_USER_MODEL)),
                ('domicilio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='humanos.Domicilio')),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_desarrollo_modificados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LugarEstacionamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('numero', models.PositiveIntegerField()),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_lugarestacionamiento_creados', to=settings.AUTH_USER_MODEL)),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lugares_estacionamiento', to='condominios.Departamento')),
                ('estorba_con', models.ManyToManyField(blank=True, related_name='_lugarestacionamiento_estorba_con_+', to='condominios.LugarEstacionamiento')),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_lugarestacionamiento_modificados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['numero'],
                'verbose_name': 'lugar de estacionamieno',
                'verbose_name_plural': 'lugares de estacionamieno',
            },
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('identificador', models.CharField(help_text='Abreviaci\xf3n que t\xedpicamente coincide con los r\xf3tulos de los botones del elevador. Por ejemplo: PB, S1, RG, 1, 2, 3, ...', max_length=8)),
                ('nombre', models.CharField(help_text='Por ejemplo: Piso 4, Planta Baja, S\xf3tano 3, Roof Garden, Piso 21', max_length=64)),
                ('numero', models.SmallIntegerField(verbose_name='n\xfamero')),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_nivel_creados', to=settings.AUTH_USER_MODEL)),
                ('desarrollo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominios.Desarrollo')),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_nivel_modificados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['numero'],
                'verbose_name_plural': 'niveles',
            },
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(db_index=True, verbose_name='fecha de inicio')),
                ('fecha_termino', models.DateField(blank=True, db_index=True, null=True, verbose_name='fecha de t\xe9rmino')),
                ('razon_termino', models.CharField(blank=True, max_length=255, null=True, verbose_name='raz\xf3n del t\xe9rmino')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_propiedad_creados', to=settings.AUTH_USER_MODEL)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propiedades', to='condominios.Departamento')),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_propiedad_modificados', to=settings.AUTH_USER_MODEL)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='humanos.Persona', verbose_name='propiedades')),
            ],
            options={
                'ordering': ['departamento'],
                'verbose_name_plural': 'propiedad',
            },
        ),
        migrations.CreateModel(
            name='Torre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('identificador', models.CharField(max_length=8)),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_torre_creados', to=settings.AUTH_USER_MODEL)),
                ('desarrollo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='torres', to='condominios.Desarrollo')),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condominios_torre_modificados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['desarrollo', 'identificador'],
            },
        ),
        migrations.AddField(
            model_name='lugarestacionamiento',
            name='nivel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lugares_estacionamiento', to='condominios.Nivel'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='nivel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departamentos', to='condominios.Nivel'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='torre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departamentos', to='condominios.Torre'),
        ),
        migrations.AlterUniqueTogether(
            name='departamento',
            unique_together=set([('torre', 'nivel', 'numero')]),
        ),
        migrations.AlterIndexTogether(
            name='departamento',
            index_together=set([('torre', 'nivel', 'numero')]),
        ),
    ]
