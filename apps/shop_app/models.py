from django.db import models
from enum import IntEnum


class UserGender(IntEnum):
    FEMALE = 0
    MALE = 1

    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))


class UsersModel(models.Model):
    name = models.CharField(max_length=32)
    name_nick = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=200)
    # shopping_cart = models.CharField(max_length=200)
    gender = models.SmallIntegerField(choices=UserGender.choices())

    def __str__(self):
        return self.name_nick

    class Meta:
        db_table = 'users'
        verbose_name = 'user'


class GoodsModel(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    origin_place = models.CharField(max_length=200)

    class Meta:
        db_table = 'goods'
        verbose_name = 'good'


class ShoppingCartModel(models.Model):
    number = models.IntegerField()
    price_all = models.IntegerField()
    user = models.ForeignKey(UsersModel, related_name="user_cart", on_delete=models.CASCADE)
    good = models.ForeignKey(GoodsModel, related_name="good_cart", on_delete=models.CASCADE)


    class Meta:
        db_table = 'shopping_cart'
        verbose_name = 'shopping_cart'



class OrderModel(models.Model):
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)
    address_person = models.CharField(max_length=200)

    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
