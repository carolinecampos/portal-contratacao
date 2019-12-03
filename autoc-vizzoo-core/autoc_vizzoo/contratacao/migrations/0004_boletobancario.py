# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-06-24 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contratacao', '0003_auto_20190621_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoletoBancario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tokenPagamento', models.CharField(max_length=50)),
                ('statusPagamento', models.IntegerField(blank=True, null=True)),
                ('numeroBoleto', models.CharField(max_length=30)),
                ('linhaDigitavel', models.CharField(max_length=70)),
                ('urlRetorno', models.CharField(max_length=2000)),
                ('dataExpiracao', models.DateField()),
                ('pagamento', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PagamentoBoleto', to='contratacao.Pagamento')),
            ],
            options={
                'db_table': 'pagamento_boleto',
            },
        ),
    ]
