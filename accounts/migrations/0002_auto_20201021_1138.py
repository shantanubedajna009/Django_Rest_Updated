# Generated by Django 2.2.3 on 2020-10-21 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='book',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='pub_year',
            field=models.IntegerField(verbose_name='Publish Year'),
        ),
    ]