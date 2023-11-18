from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand','unit_price','catagorie']
    list_editable=['unit_price']
    list_per_page= 6
admin.site.register(Catagories)
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

