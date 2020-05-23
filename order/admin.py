from django.contrib import admin

# Register your models here.
from order.models import OrderProduct, Order


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'status']
    list_filter = ['status']
    readonly_fields = ['user', 'address', 'city', 'country', 'phone', 'first_name', 'ip', 'last_name', 'phone']
    can_delete = False
    inlines = [OrderProductline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price']
    list_filter = ['user']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
