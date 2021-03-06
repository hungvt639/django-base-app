# Generated by Django 3.0.4 on 2021-07-26 16:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusers',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='time create'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myusers',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='time update'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='avatar',
            field=models.FileField(blank=True, default='avatar.jpg', null=True, upload_to='image/avatar', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='birthday'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='email',
            field=models.EmailField(max_length=200, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Nam'), (2, 'Nữ'), (0, 'Khác')], default=1, null=True, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='phone'),
        ),
    ]
