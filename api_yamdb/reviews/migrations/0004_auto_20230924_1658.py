# Generated by Django 3.2 on 2023-09-24 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230922_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Рейтинг'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=10, message='Не более 10 баллов.'), django.core.validators.MinValueValidator(limit_value=1, message='Не менее 1 балла.')], verbose_name='Рейтинг'),
        ),
    ]
