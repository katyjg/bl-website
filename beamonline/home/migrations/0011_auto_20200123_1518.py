# Generated by Django 3.0.2 on 2020-01-23 15:18

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='call',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
