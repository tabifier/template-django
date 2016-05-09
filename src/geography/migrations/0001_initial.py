# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('currency_code', models.CharField(blank=True, max_length=3, null=True)),
                ('currency_name', models.CharField(blank=True, max_length=50, null=True)),
                ('dial_code', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.Country')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]