# Generated by Django 4.0.2 on 2022-10-23 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saleapp', '0012_remove_orderdetail_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Momo', 'Momo'), ('COD', 'COD')], default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ToReceive', 'ToReceive'), ('Completed', 'Completed')], default='ToReceive', max_length=30),
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
    ]
