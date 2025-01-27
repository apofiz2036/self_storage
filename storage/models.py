from django.db import models
from datetime import timedelta


class Warehouse(models.Model):
    name = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Название склада'
    )
    address = models.TextField(verbose_name='Адрес склада')
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активен'
    )
    
    def __str__(self):
        return f"{self.name} ({self.address})"

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'Склады'


class StorageBoxType(models.Model):
    BOX_TYPES = [
        ('SMALL', 'Малый (<1м³)'),
        ('MEDIUM', 'Средний (1м³-5м³)'),
        ('LARGE', 'Большой (5м³<)'),
    ]
    
    warehouse = models.ForeignKey(
        Warehouse, 
        on_delete=models.CASCADE, 
        related_name='box_types',
        verbose_name='Склад'
    )
    name = models.CharField(
        max_length=20, 
        choices=BOX_TYPES,
        verbose_name='Тип бокса'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Цена'
    )
    dimensions = models.CharField(
        max_length=50,
        verbose_name='Габариты'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    class Meta:
        unique_together = ('warehouse', 'name')
        verbose_name = 'тип бокса'
        verbose_name_plural = 'Типы боксов'

    def __str__(self):
        return f"{self.get_name_display()} ({self.warehouse.name})"


class StorageBox(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, 
        on_delete=models.CASCADE, 
        related_name='boxes',
        verbose_name='Склад'
    )
    box_type = models.ForeignKey(
        StorageBoxType, 
        on_delete=models.CASCADE,
        verbose_name='Тип бокса'
    )
    box_number = models.CharField(
        max_length=10,
        verbose_name='Номер бокса'
    )
    is_occupied = models.BooleanField(
        default=False,
        verbose_name='Занят'
    )
    current_order = models.OneToOneField(
        'Order', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_box',
        verbose_name='Текущий заказ'
    )
    
    def get_status(self):
        if self.current_order and self.is_occupied:
            return f"Занят до {self.current_order.expires_at.strftime('%d.%m.%Y')}"
        return "Свободен"
    
    def __str__(self):
        return f"{self.warehouse.name} - {self.box_number} ({self.box_type.get_name_display()})"

    class Meta:
        verbose_name = 'бокс'
        verbose_name_plural = 'Боксы'


class Clients(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='ФИО клиента'
    )
    phone_number = models.CharField(
        max_length=15, 
        verbose_name='Телефон клиента'
    )
    telegram_id = models.PositiveBigIntegerField(
        unique=True, 
        null=True,
        verbose_name='Telegram ID'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    ORDER_STATUSES = [
        ('NEW', 'Новый'),
        ('DELIVERY', 'В доставке'),
        ('STORED', 'На хранении'),
        ('EXPIRED', 'Просрочен'),
        ('COMPLETED', 'Завершен'),
    ]
    
    VOLUME_CHOICES = [
        ('S', 'Малый (до 1м³)'),
        ('M', 'Средний (1-5м³)'),
        ('L', 'Большой (5-10м³)'),
    ]
    
    user = models.ForeignKey(
        Clients, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name='Клиент'
    )
    volume = models.CharField(
        max_length=20, 
        choices=VOLUME_CHOICES,
        verbose_name='Объем'
    )
    address_from = models.TextField(
        verbose_name='Адрес забора'
    )
    delivery_type = models.CharField(
        max_length=20,
        choices=[('PICKUP', 'Самовывоз'), ('DELIVERY', 'Доставка')],
        verbose_name='Тип доставки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    expires_at = models.DateTimeField(
        verbose_name='Дата окончания хранения'
    )
    final_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Итоговая цена'
    )
    qr_code = models.ImageField(
        upload_to='qr_codes/', 
        blank=True,
        verbose_name='QR-код'
    )
    warehouse = models.ForeignKey(
        Warehouse, 
        on_delete=models.CASCADE, 
        null=True,
        verbose_name='Склад'
    )
    box = models.ForeignKey(
        StorageBox, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Бокс'
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUSES,
        default='NEW',
        verbose_name='Статус'
    )
    reminder_1 = models.DateTimeField(
        editable=False, 
        null=True,
        verbose_name='Первое напоминание'
    )
    reminder_2 = models.DateTimeField(
        editable=False, 
        null=True,
        verbose_name='Второе напоминание'
    )
    reminder_3 = models.DateTimeField(
        editable=False, 
        null=True,
        verbose_name='Третье напоминание'
    )
    reminder_4 = models.DateTimeField(
        editable=False, 
        null=True,
        verbose_name='Четвертое напоминание'
    )

    def save(self, *args, **kwargs):
        if self.expires_at:
            self.reminder_1 = self.expires_at - timedelta(days=30)
            self.reminder_2 = self.expires_at - timedelta(days=14)
            self.reminder_3 = self.expires_at - timedelta(days=7)
            self.reminder_4 = self.expires_at - timedelta(days=3)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.name}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
