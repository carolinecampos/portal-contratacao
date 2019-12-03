# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-11-22 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratacao', '0005_auto_20190625_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_remetente', models.CharField(blank=True, max_length=100, null=True)),
                ('assunto', models.CharField(max_length=200)),
                ('email_destinatario', models.CharField(max_length=100)),
                ('nome_destinatario', models.CharField(blank=True, max_length=100, null=True)),
                ('corpo', models.TextField()),
                ('tipo_template', models.CharField(choices=[('confirmacao_adiquirentes', 'confirmacao adiquirentes')], max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='grupo',
            name='nome_fantasia',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]