from rest_framework import serializers
from apps.shop_app.models import UsersModel, ShoppingCartModel, GoodsModel, OrderModel, UserGender


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, error_messages={'blank': 'name is error.'})
    name_nick = serializers.CharField(max_length=32, error_messages={'blank': 'name_nick is error.'})
    password = serializers.CharField(max_length=32, error_messages={'blank': 'password is error.'})
    email = serializers.EmailField(max_length=200, error_messages={'blank': 'email is error.'})
    gender = serializers.ChoiceField(choices=[item.value for item in UserGender], error_messages={'blank': 'gender is error.'})

    def validate(self, attrs):
        name_nick = attrs.get("name_nick")
        if UsersModel.objects.filter(name_nick=name_nick).exists():
            raise serializers.ValidationError("User already exists")
        return attrs


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersModel
        fields = "__all__"


class CreateGoodSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, error_messages={'blank': 'name is error.'})
    price = serializers.CharField(max_length=32, error_messages={'blank': 'price is error.'})
    origin_place = serializers.CharField(max_length=32, error_messages={'blank': 'origin_place is error.'})


class GoodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsModel
        fields = "__all__"


class CreateCartSerializere(serializers.Serializer):
    number = serializers.IntegerField()
    price_all = serializers.IntegerField()


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class CreateOrderSerializere(serializers.Serializer):
    address = serializers.CharField()
    user_phone = serializers.CharField()
    # number = serializers.IntegerField()
    # price = serializers.IntegerField()
    # good_name = serializers.CharField()
    name_nick = serializers.CharField()

