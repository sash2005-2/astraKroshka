from django.contrib import admin

# Register your models here.
from .models import Category, Brand, Product, CartItem, Cart, Order


class CategoryAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Category, CategoryAdmin)


#admin.site.register(Category)
admin.site.register(Brand)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
#admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)