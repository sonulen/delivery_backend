# Generated by Django 3.1.1 on 2020-09-12 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_recipient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_created_datetime', models.DateTimeField(auto_now_add=True)),
                ('delivery_datetime', models.DateTimeField()),
                ('status', models.CharField(choices=[('Created', 'Создан'), ('Delivered', 'Доставлен'), ('Processed', 'Обработан'), ('Cancelled', 'Отменен')], default='Created', max_length=24)),
                ('product_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='repository.productsets')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='repository.recipient')),
            ],
        ),
    ]
