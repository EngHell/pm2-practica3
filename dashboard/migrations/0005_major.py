# Generated by Django 3.1.7 on 2021-03-18 20:19

from django.db import migrations, models


def seed_database(apps, schema_editor):
    Major = apps.get_model('dashboard', 'Major')
    Major(code='M01', name='Matematica').save()
    Major(code='F01', name='Fisica').save()

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20210318_0708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RunPython(seed_database)
    ]
