# Generated by Django 2.2.3 on 2020-10-15 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statusmodel',
            options={'verbose_name': 'status', 'verbose_name_plural': 'statuses'},
        ),
    ]