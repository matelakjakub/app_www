# Generated by Django 4.2.6 on 2023-10-23 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_stanowisko_osoba'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='osoba',
            table='Osoba',
        ),
        migrations.AlterModelTable(
            name='stanowisko',
            table='Stanowisko',
        ),
    ]
