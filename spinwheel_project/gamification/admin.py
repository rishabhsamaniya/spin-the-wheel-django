from django.contrib import admin
from .models import User, Category, Product, Spin, Address, Order
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Spin)
admin.site.register(Address)
admin.site.register(Order)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available')
