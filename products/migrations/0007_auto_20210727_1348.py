# Generated by Django 3.2.5 on 2021-07-27 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('products', '0006_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='mobile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.usermobileno'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_date_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
