from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, HiddenField, CurrentUserDefault, IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import Region, District, Category, User, Seller
from apps.models.utils import uz_phone_validator
from apps.tasks import register_key, generate_random_password, send_sms_code


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        # fields = '__all__'
        exclude = 'region',


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'birth_date', 'email']


class UserProfileUpdateModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'birth_date']


class UserChangePasswordModelSerializer(ModelSerializer):
    old_password = CharField(max_length=255)
    confirm_password = CharField(max_length=255)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'confirm_password']

    def validate(self, attrs: dict):

        for i in set(self.Meta.fields):
            if i not in attrs:
                raise ValidationError(f"{i} field is required")

        old_password = attrs.get('old_password')
        confirm_password = attrs.get('confirm_password')
        password = attrs.get('password')
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise ValidationError("Old password is not correct")

        if password != confirm_password:
            raise ValidationError('Passwords do not match')
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('old_password', None)
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)


class UserRegisterModelSerializer(ModelSerializer):
    code = IntegerField(min_value=10_000, max_value=99_9999, write_only=True)
    phone = CharField(max_length=15, validators=[uz_phone_validator])

    class Meta:
        model = User
        fields = ['phone', 'code']
        extra_kwargs = {
            'phone': {'write_only': True}
        }

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise ValidationError("Phone number already exists")
        return value

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.pop('code', None)
        cache_code = cache.get(register_key(phone))
        if code != cache_code:
            raise ValidationError("Wrong code")
        return attrs

    def create(self, validated_data):
        validated_data.pop('code', None)
        phone = validated_data.get('phone')
        password = generate_random_password()
        validated_data['password'] = make_password(password)
        text = f"Bu sizning parolingiz {password}"
        send_sms_code.enqueue(phone, text)
        self.user = super().create(validated_data)
        self.user.first_name = f'user-{self.user.id}'
        self.user.save(update_fields=['first_name'])
        return self.user

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        refresh = RefreshToken.for_user(self.user)
        repr["refresh"] = str(refresh)
        repr["access"] = str(refresh.access_token)
        repr["data"] = UserModelSerializer(self.user).data
        return repr


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', ]

        read_only_fields = []
        # extra_kwargs = {
        #     'address': {'write_only': True}
        # }


class SellerModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Seller
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["data"] = UserModelSerializer(self.user).data

        return data

#
#
# class ProductListModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'discount', 'in_stock']
#
#
# class ProductCreateModelSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'discount', 'quantity', 'category']
#
#
# class UserModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'username', 'phone']
#
#
# class OrderModelSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
