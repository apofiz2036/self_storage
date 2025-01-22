from django.contrib import admin
from .models import *


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_active')


@admin.register(StorageBoxType)
class StorageBoxTypeAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse', 'get_name_display', 'price')
    list_filter = ('warehouse',)
    
    def get_warehouse(self, obj):
        return obj.warehouse.name
    get_warehouse.short_description = 'Склад'


@admin.register(StorageBox)
class StorageBoxAdmin(admin.ModelAdmin):
    list_display = ('box_number', 'get_warehouse', 'box_type', 'get_status')
    list_filter = ('warehouse', 'box_type')
    raw_id_fields = ('current_order',)

    def get_warehouse(self, obj):
        return obj.warehouse.name
    get_warehouse.short_description = 'Склад'
    
    def get_status(self, obj):
        return obj.get_status()
    get_status.short_description = 'Статус'


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'get_client', 
        'volume', 
        'delivery_type', 
        'expires_at', 
        'warehouse_address'
    )
    readonly_fields = ('reminder_1', 'reminder_2', 'reminder_3', 'reminder_4')
    search_fields = ('user__name', 'user__phone_number')
    raw_id_fields = ('user', 'box')

    def get_client(self, obj):
        return obj.user.name
    get_client.short_description = 'Имя клиента'

    def warehouse_address(self, obj):
        return obj.warehouse.address
    warehouse_address.short_description = 'Адрес склада'

