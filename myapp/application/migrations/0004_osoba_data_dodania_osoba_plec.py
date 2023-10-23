# Generated by Django 4.2.6 on 2023-10-23 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_osoba_table_alter_stanowisko_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='osoba',
            name='data_dodania',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='osoba',
            name='plec',
            field=models.IntegerField(choices=[(1, 'Mezczyzna'), (2, 'Kobieta'), (3, 'Inne')], default=1),
            preserve_default=False,
        ),
    ]