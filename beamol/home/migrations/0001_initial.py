# Generated by Django 3.0.3 on 2020-02-05 16:35

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailimages', '0001_squashed_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneColumnPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubsitePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TwoColumnPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True)),
                ('sidebar', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SubsiteHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True)),
                ('name_short', models.CharField(blank=True, max_length=40)),
                ('name_long', models.CharField(blank=True, max_length=100)),
                ('meta_description', models.CharField(blank=True, max_length=500)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('organization', models.CharField(blank=True, max_length=100)),
                ('org_url', models.URLField(blank=True, verbose_name='Organization link')),
                ('footer1', wagtail.fields.RichTextField(blank=True)),
                ('footer2', wagtail.fields.RichTextField(blank=True)),
                ('header_color', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('footer_color', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('org_img', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('call', wagtail.fields.RichTextField(blank=True)),
                ('announcements', wagtail.fields.RichTextField(blank=True)),
                ('footer1', wagtail.fields.RichTextField(blank=True)),
                ('footer2', wagtail.fields.RichTextField(blank=True)),
                ('column1', wagtail.fields.RichTextField(blank=True)),
                ('column2', wagtail.fields.RichTextField(blank=True)),
                ('name_short', models.CharField(blank=True, max_length=40)),
                ('name_long', models.CharField(blank=True, max_length=100)),
                ('meta_description', models.CharField(blank=True, max_length=500)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('organization', models.CharField(blank=True, max_length=100)),
                ('org_url', models.URLField(blank=True, verbose_name='Organization link')),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('org_img', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
