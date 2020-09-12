# Generated by Django 3.1.1 on 2020-09-12 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='repository.productsets'),
        ),
    ]
