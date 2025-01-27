# Generated by Django 4.2.18 on 2025-01-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_order_storagebox_storageboxtype_remove_orders_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый'), ('DELIVERY', 'В доставке'), ('STORED', 'На хранении'), ('EXPIRED', 'Просрочен'), ('COMPLETED', 'Завершен')], default='NEW', max_length=20, verbose_name='Статус'),
        ),
    ]
