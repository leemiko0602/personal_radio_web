# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
            ],
            options={
                'managed': False,
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=500)),
                ('replies', models.IntegerField(blank=True, null=True)),
                ('retweets', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'feed',
            },
        ),
        migrations.CreateModel(
            name='LiveRadioDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'live_radio_dictionary',
            },
        ),
        migrations.CreateModel(
            name='RadioProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.IntegerField(blank=True, null=True)),
                ('subject', models.IntegerField(blank=True, null=True)),
                ('key_words', models.CharField(blank=True, max_length=255, null=True)),
                ('compere', models.CharField(blank=True, max_length=45, null=True)),
                ('guests', models.CharField(blank=True, max_length=255, null=True)),
                ('file_name', models.CharField(max_length=45)),
                ('server_name', models.CharField(max_length=45)),
                ('share_name', models.CharField(max_length=45)),
                ('directory', models.CharField(max_length=255)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'radio_program',
            },
        ),
        migrations.CreateModel(
            name='SubjectUserProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=45)),
                ('describe', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'subject_user_program',
            },
        ),
    ]