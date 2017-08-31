# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True)),
                ('meta', models.TextField(default=b'{}')),
                ('name', models.CharField(max_length=127)),
                ('smtp_id', models.CharField(max_length=127)),
                ('sg_event_id', models.CharField(max_length=127)),
                ('sg_message_id', models.CharField(max_length=127)),
                ('timestamp', models.DateTimeField()),
                ('email', models.CharField(blank=True, default=b'', max_length=127, null=True)),
                ('category', models.CharField(blank=True, default=b'', max_length=127, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True)),
                ('meta', models.TextField(default=b'{}')),
                ('customer_id', models.PositiveIntegerField()),
                ('email_from_name', models.CharField(default=b'No Reply', max_length=63)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IncomingMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True)),
                ('meta', models.TextField(default=b'{}')),
                ('mail_from', models.CharField(max_length=127)),
                ('mail_to', models.CharField(max_length=127)),
                ('mail_cc', models.CharField(max_length=127)),
                ('subject', models.CharField(max_length=127)),
                ('attachments', models.TextField(default=b'{}')),
                ('info', models.TextField(default=b'{}')),
                ('text', models.TextField(null=True)),
                ('html', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SGMessageIdLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True)),
                ('meta', models.TextField(default=b'{}')),
                ('object_id', models.CharField(max_length=127)),
                ('object_type', models.CharField(max_length=127)),
                ('sg_message_id', models.CharField(max_length=127)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
