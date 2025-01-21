from django.db import models
from datetime import timedelta


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название статуса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'Статусы'


class Warehouse(models.Model):
    address = models.CharField(
        max_length=200, verbose_name='Адрес склада'
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'Склады'


class Clients(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='ФИО клиента'
    )
    phone_number = models.CharField(
        max_length=15, verbose_name='Телефон клиента'
    )
    address = models.CharField(
        max_length=200, verbose_name='Адрес склада'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'


class Orders(models.Model):
    date_start = models.DateField(
        blank=True, null=True, verbose_name='Дата начала хранения'
    )
    date_final = models.DateField(
        blank=True, null=True, verbose_name='Дата окончания хранения'
    )
    client = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Склад'
    )

    reminder_1 = models.DateTimeField(
        editable=False, verbose_name='Первое напоминание', null=True
    )
    reminder_2 = models.DateTimeField(
        editable=False, verbose_name='Второе напоминание', null=True
    )
    reminder_3 = models.DateTimeField(
        editable=False, verbose_name='Третье напоминание', null=True
    )
    reminder_4 = models.DateTimeField(
        editable=False, verbose_name='Четвертое напоминание', null=True
    )

    def save(self, *args, **kwargs):
        if self.date_final:
            self.reminder_1 = self.date_final - timedelta(days=30)
            self.reminder_2 = self.date_final - timedelta(days=14)
            self.reminder_3 = self.date_final - timedelta(days=7)
            self.reminder_4 = self.date_final - timedelta(days=3)
        super().save(*args, **kwargs)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
