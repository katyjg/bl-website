# Generated by Django 3.0.5 on 2020-04-27 19:55

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('beamlines', '0004_embedpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeamlineDisplayPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True)),
                ('gallery', wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock(icon='image'))], blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='beamlinepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))]),
        ),
        migrations.AlterField(
            model_name='beamlinepage',
            name='gallery',
            field=wagtail.fields.StreamField([('image', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.TextBlock(required=False))]), icon='image', template='beamlines/blocks/gallery.html'))], blank=True, null=True),
        ),
    ]
