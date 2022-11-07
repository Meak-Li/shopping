import json
import time
from django.http import JsonResponse

from apps.shop_app.models import UsersModel, ShoppingCartModel, GoodsModel, OrderModel
from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

from apps.shop_app.serializers import CreateUserSerializer, UserModelSerializer, CreateGoodSerializer, \
    GoodModelSerializer, CreateCartSerializere, OrderModelSerializer, CreateOrderSerializere


class UsersView(APIView):
    """用户操作"""

    def get(self, request):
        name_nick_query = request.GET.get('name_nick')

        if name_nick_query is None:
            return Response({
                "code": 404,
                "message": "name_nick needs a value",
            })

        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        users = UsersModel.objects.filter(name_nick__istartswith=name_nick_query)
        total_count = users.count()
        _users = users[offset:offset + limit]
        user_data = UserModelSerializer(_users, many=True).data

        return Response({
            "code": 200,
            "message": "Success",
            "data": {
                "list": user_data,
                "pagination": {
                    "total_count": total_count,
                    "offset": offset,
                    "limit": limit,
                }
            }
        })

    def post(self, request):
        """用户注册"""
        user_data = json.loads(request.body)
        serializers = CreateUserSerializer(data={
            "name": user_data.get("name"),
            "name_nick": user_data.get("name_nick"),
            "password": user_data.get("password"),
            "email": user_data.get("email"),
            "gender": user_data.get("gender"),
        })

        if not serializers.is_valid():
            return Response(serializers.errors)

        _name_nick = UsersModel.objects.filter(name_nick=user_data["name_nick"]).first()
        if _name_nick:
            return Response("用户名已经存在")

        user = UsersModel.objects.create(
            name=user_data["name"],
            name_nick=user_data["name_nick"],
            password=user_data["password"],
            email=user_data["email"],
            gender=user_data["gender"],
        )

        if user.gender == 1:
            gender_out = "male"
        else:
            gender_out = "female"

        return JsonResponse({
            "code": 200,
            "message": "Success",
            "data": {
                "user": user.id,
                "name_nick": user.name_nick,
                "email": user.email,
                "gender": gender_out,
            }
        })

    def put(self, request):
        name_nick_query = request.GET.get('name_nick')
        password_query = request.META.get('HTTP_PASSWORD')
        # users = UsersModel.objects.filter(name_nick=name_nick_query)
        UsersModel.objects.filter(name_nick=name_nick_query).update(password=password_query)
        # UsersModel.save()
        return JsonResponse({
            "code": 200,
            "message": "Success",
            "data": {
                "name_nick": name_nick_query,
                "password": "success"
            }
        })


class UserLoginView(APIView):
    authentication_classes = ()

    def post(self, request):
        data = json.loads(request.body)
        name_nick = data.get("name_nick")
        user = UsersModel.objects.filter(name_nick=name_nick).first()
        if not user:
            return Response({
                "code": 404,
                "message": "Not Found"
            })
        payload = {
            "name_nick": name_nick,
            "exp": int(time.time()) + 10000000 * 60
        }

        from django.conf import settings
        import jwt
        secret_key = settings.SECRET_KEY
        token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")

        return Response({
            "code": 200,
            "message": "Success",
            "data": {
                "token": token
            }
        })


class GoodsView(APIView):
    def get(self, request):
        name_query = request.GET.get('name')
        goods_all = GoodsModel.objects.filter()
        good_data_all = GoodModelSerializer(goods_all, many=True).data
        if name_query is None:
            # return Response({
            #     "code": 404,
            #     "message": "name needs a value",
            # })
            return Response({
                "code": 200,
                "message": "success",
                "data": {
                    "list": good_data_all
                }
            })

        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        goods = GoodsModel.objects.filter(name__istartswith=name_query)
        total_count = goods.count()
        _goods = goods[offset:offset + limit]
        good_data = GoodModelSerializer(_goods, many=True).data

        return Response({
            "code": 200,
            "message": "Success",
            "data": {
                "list": good_data,
                "pagination": {
                    "total_count": total_count,
                    "offset": offset,
                    "limit": limit,
                }
            }
        })

    def post(self, request):
        """添加商品"""
        good_data = json.loads(request.body)
        serializers = CreateGoodSerializer(data={
            "name": good_data.get("name"),
            "price": good_data.get("price"),
            "origin_place": good_data.get("origin_place"),
        })

        if not serializers.is_valid():
            return Response(serializers.errors)

        _good_name = GoodsModel.objects.filter(name=good_data["name"]).first()
        if _good_name:
            return Response("商品已经存在")

        good = GoodsModel.objects.create(
            name=good_data["name"],
            price=good_data["price"],
            origin_place=good_data["origin_place"],
        )
        return JsonResponse({
            "code": 200,
            "message": "Success",
            "data": {
                "user": good.id,
                "name_nick": good.price,
                "email": good.origin_place,
            }
        })


class ShoppingCartView(APIView):
    def get(self, request):
        # 查看购物车，需要传入一个name_nick
        carts = ShoppingCartModel.objects.all()
        user_nick_query = request.GET.get("name_nick")

        return Response(
            [{
                "user_id": cart.user.id,
                "user_nick": cart.user.name_nick,
                "good_id": cart.good.id,
                "good": cart.good.name,
            } for cart in carts if cart.user.name_nick == user_nick_query
            ]
        )

    def post(self, request):
        # 添加购物车
        cart_data = json.loads(request.body)
        name_nick_query = cart_data.get("name_nick")
        good_name_query = cart_data.get("good_name")
        # 生成实例化对象
        user_obj = UsersModel.objects.filter(name_nick=name_nick_query).first()
        good_obj = GoodsModel.objects.filter(name=good_name_query).first()
        # 计算价格
        price_all = good_obj.price * cart_data.get("number")
        serializers = CreateCartSerializere(data={
            "number": cart_data.get("number"),
            "price_all": price_all,
            # "good_id": cart_data.get("good_id"),
            # "user_id": cart_data.get("user_id"),
        })
        if not serializers.is_valid():
            return Response(serializers.errors)
        # 注意这里user与good需要传入一个实例化对象
        cart = ShoppingCartModel.objects.create(
            number=cart_data["number"],
            price_all=price_all,
            user=user_obj,
            good=good_obj,
        )

        return JsonResponse({
            "code": 200,
            "message": "Success",
            "data": {
                "cart": cart.id,
                "user_id": cart.user.id,
                "user_nick": cart.user.name_nick,
                "good_id": cart.good.id,
                "good_name": cart.good.name,
                "price_all": cart.good.price_all
            }
        })

    def put(self, request):
        # 修改购物车里面的物品（主要是个数的修改）
        data = json.loads(request.body)
        name_nick_query = data.get("name_nick")
        good_name_query = data.get("good_name")
        number = data.get("number")
        # 查找到具体的user
        user = UsersModel.objects.filter(name_nick=name_nick_query).first()
        # 获取所有的购物车里面的对象
        user_all = user.user_cart.all()
        # 遍历所有的对象，获取符合条件的物品
        for user_cart in user_all:
            print(user_cart.good.name)
            if user_cart.good.name == good_name_query:
                good_id = user_cart.id
                print(good_id)
                print(type(good_id))
                ShoppingCartModel.objects.filter(id=good_id).update(number=number)
                break

        return Response("success")

    def delete(self, request):
        # 修改购物车里面的物品（主要是个数的修改）
        data = json.loads(request.body)
        name_nick_query = data.get("name_nick")
        good_name_query = data.get("good_name")
        # 查找到具体的user
        user = UsersModel.objects.filter(name_nick=name_nick_query).first()
        # 获取所有的购物车里面的对象
        user_all = user.user_cart.all()
        # 遍历所有的对象，获取符合条件的物品
        for user_cart in user_all:
            print(user_cart.good.id)
            if user_cart.good.name == good_name_query:
                # 删除物品
                user_cart.delete()
        return Response("success")

        # if not ShoppingCartModel.user.objects.filter(name_nick=name_nick_query).exists():
        #     return Response("user not found or not cart")
        # if not ShoppingCartModel.good.objects.filter(good_name=good_name_query).exists():
        #     return Response("good not found")
        #
        # user = UsersModel.objects.filter(name=name_nick_query).first()
        #
        # user.user_cart.good.filter(name=good_name_query).delete()


class OrdersView(APIView):
    def get(self, request):
        # 查看订单(凭手机号查订单)
        phone_query = request.GET.get('phone')
        # orders_all = OrderModel.objects.all()
        # order_data_all = OrderModelSerializer(orders_all, many=True).data

        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        orders = OrderModel.objects.filter(user_phone=phone_query)
        total_count = orders.count()
        _orders = orders[offset:offset + limit]
        order_data = OrderModelSerializer(_orders, many=True).data
        return Response({
            "code": 200,
            "message": "Success",
            "data": {
                "list": order_data,
                "pagination": {
                    "total_count": total_count,
                    "offset": offset,
                    "limit": limit,
                }
            }
        })

    def post(self, request):
        # 下单，走购物车下单
        data = json.loads(request.body)

        serializers = CreateOrderSerializere(data={
            "address": data.get("address"),
            "user_phone": data.get("user_phone"),
            "number": data.get("number"),
            "price": data.get("price"),
            "good_name": data.get("good_name"),
            "name_nick": data.get("name_nick")
        })
        if not serializers.is_valid():
            return Response(serializers.errors)

        name_nick_query = data.get("name_nick")
        good_name_query = data.get("good_name")

        user_obj = UsersModel.objects.filter(name_nick=name_nick_query).first()
        good_obj = GoodsModel.objects.filter(name=good_name_query).first()

        order = OrderModel.objects.create(
            address=data["address"],
            user_phone=data["user_phone"],
            number=data["number"],
            price=data["price"],
            user=user_obj,
            good=good_obj
        )

        return Response({
            "code": 200,
            "message": "Success",
            "data": {
                "name_nick": order.user.name_nick,
                "good_name": order.good.name,
                "address": order.address,
                "phone": order.user_phone,
                "number": order.number,
                "price": order.price
            }
        })
