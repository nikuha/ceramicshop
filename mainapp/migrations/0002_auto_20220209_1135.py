# Generated by Django 3.2.9 on 2022-02-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='is_active',
            field=models.BooleanField(db_index=True, default=1, verbose_name='активный'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=1, verbose_name='активная'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=1, verbose_name='активная'),
        ),
    ]