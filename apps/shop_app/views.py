import json
import time
from django.http import JsonResponse

from apps.shop_app.models import UsersModel, ShoppingCartModel, GoodsModel, OrderModel
from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

from apps.shop_app.serializers import CreateUserSerializer, UserModelSerializer, CreateGoodSerializer, GoodModelSerializer


class UsersView(APIView):
    """用户"""

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
    pass
