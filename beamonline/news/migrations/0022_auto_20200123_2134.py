# Generated by Django 3.0.2 on 2020-01-23 21:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_auto_20200123_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpage',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 1, 23, 21, 34, 4, 653737, tzinfo=utc)),
        ),
    ]
