# Generated by Django 3.0.3 on 2020-02-06 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beamlines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationspage',
            name='latest_api',
            field=models.URLField(blank=True),
        ),
    ]
