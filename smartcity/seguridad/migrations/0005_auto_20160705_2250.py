# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 22:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('humanos', '0003_auto_20160705_2230'),
        ('seguridad', '0004_auto_20160705_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(db_index=True, verbose_name='fecha de inicio')),
                ('fecha_termino', models.DateField(blank=True, db_index=True, null=True, verbose_name='fecha de t\xe9rmino')),
                ('razon_termino', models.CharField(blank=True, max_length=255, null=True, verbose_name='raz\xf3n del t\xe9rmino')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='\xfaltima modificaci\xf3n')),
                ('resolucion', models.NullBooleanField(verbose_name='resoluci\xf3n')),
                ('fecha_resolucion', models.DateTimeField(blank=True, null=True, verbose_name='fecha de la resoluci\xf3n')),
                ('contenido', models.TextField()),
                ('a_favor', models.ManyToManyField(blank=True, related_name='propuestas_a_favor', to='humanos.Persona')),
                ('contrapropuesta_de', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contrapropuestas', to='seguridad.Propuesta')),
                ('creado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seguridad_propuesta_creados', to=settings.AUTH_USER_MODEL)),
                ('en_contra', models.ManyToManyField(blank=True, related_name='propuestas_en_contra', to='humanos.Persona')),
                ('iniciado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iniciativas_iniciadas', to='humanos.Persona')),
                ('modificado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seguridad_propuesta_modificados', to=settings.AUTH_USER_MODEL)),
                ('neutrales', models.ManyToManyField(blank=True, related_name='propuestas_neutrales', to='humanos.Persona')),
            ],
            options={
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.RemoveField(
            model_name='iniciativa',
            name='a_favor',
        ),
        migrations.RemoveField(
            model_name='iniciativa',
            name='creado_por',
        ),
        migrations.RemoveField(
            model_name='iniciativa',
            name='en_contra',
        ),
        migrations.RemoveField(
            model_name='iniciativa',
            name='iniciado_por',
        ),
        migrations.RemoveField(
            model_name='iniciativa',
            name='modificado_por',
        ),
        migrations.RemoveField(
            model_name='iniciativa',
            name='neutrales',
        ),
        migrations.RenameField(
            model_name='comentario',
            old_name='comentario',
            new_name='contenido',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='iniciativa',
        ),
        migrations.DeleteModel(
            name='Iniciativa',
        ),
        migrations.AddField(
            model_name='comentario',
            name='propuesta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='seguridad.Propuesta'),
            preserve_default=False,
        ),
    ]
