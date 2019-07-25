# Generated by Django 2.2.2 on 2019-06-11 17:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('stations', django.contrib.postgres.fields.jsonb.JSONField()),
                ('weather', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]