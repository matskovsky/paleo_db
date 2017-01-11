# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-04 21:29
from __future__ import unicode_literals

import db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='description',
            name='genus',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='group',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='species',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='speciesAuthor',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='speciesYear',
            field=models.CharField(max_length=4, null=True, validators=[db.models.validate_year]),
        ),
        migrations.AddField(
            model_name='description',
            name='subgenus',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='subspecies',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='subspeciesAuthor',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='description',
            name='subspeciesYear',
            field=models.CharField(max_length=4, null=True, validators=[db.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='sample',
            name='country',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='geologicalContext',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='gorizont',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='region',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='regionSpec',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sistema',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sloy',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='svita',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='yarus',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='genus',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='group',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='species',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='speciesAuthor',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='speciesYear',
            field=models.CharField(max_length=4, null=True, validators=[db.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='subgenus',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='subspecies',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='taxon',
            name='subspeciesAuthor',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
