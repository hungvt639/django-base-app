# Generated by Django 3.2.3 on 2021-09-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20210726_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myusers',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
