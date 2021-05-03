# Generated by Django 3.1.7 on 2021-03-18 07:08

from django.db import migrations


def create_basic_genres(apps, schema_editor):
        StudentGenre = apps.get_model('dashboard', 'StudentGenre')

        StudentGenre(name='Masculino').save()
        StudentGenre(name='Femenino').save()
        StudentGenre(name='Otro').save()


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20210318_0704'),
    ]

    operations = [
        migrations.RunPython(create_basic_genres)
    ]
