from django.contrib import admin
from django.contrib.auth.models import User, Group
from apps.shop_app.models import UsersModel, ShoppingCartModel, GoodsModel, OrderModel

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(UsersModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name_nick", "email", "gender"]
    search_fields = ["name_nick"]
    list_filter = ["gender"]


@admin.register(ShoppingCartModel)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["user", "good", "number", "price_all"]
    search_fields = ["user"]
    list_filter = ["user"]


@admin.register(GoodsModel)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "origin_place"]
    search_fields = ["name"]
    list_filter = ["origin_place"]


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["address", "email", "phone", "sender", "address_person"]
    search_fields = ["phone"]