# Generated by Django 3.2.5 on 2022-09-12 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20220912_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
