# Generated by Django 3.0.2 on 2020-01-23 16:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_auto_20200123_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpage',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 1, 23, 16, 18, 47, 10792, tzinfo=utc)),
        ),
    ]
