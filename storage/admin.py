from django.contrib import admin
from .models import OrderStatus, Warehouse, Clients, Orders


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('address',)


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'client_name',
        'date_start',
        'date_final',
        'warehouse_address'
    )
    readonly_fields = ('reminder_1', 'reminder_2', 'reminder_3', 'reminder_4')

    def client_name(self, obj):
        return obj.client.name
    client_name.short_description = 'Имя клиента'

    def warehouse_address(self, obj):
        return obj.warehouse.address
    warehouse_address.short_description = 'Адрес склада'


admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Orders, OrdersAdmin)