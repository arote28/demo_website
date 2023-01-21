from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # import pdb;
        # pdb.set_trace()
        # if validated_data['role'] == 1:
        #     auth_user = User.objects.create_superuser(**validated_data)
        #     return auth_user
        # else:
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UserDetailSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=False)
    # password = serializers.CharField(max_length=200, required=False)
    # mobile_number = serializers.CharField(max_length=12,required=False)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs ={
            "password":{"write_only":True}
        }

# class UserAuthSerializer(serializers.ModelSerializer):
#     auth_token = serializers.SerializerMethodField()
#     email = serializers.EmailField(required=False)
#     password = serializers.CharField(max_length=200, required=False)
#     mobile_number = serializers.CharField(max_length=12,required=False)
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def get_auth_token(self,obj):
#         token = Token.objects.create(user=obj)
#         return token.key
#
# class EmptySerializer(serializers.Serializer):
#     pass



# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email','password']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(email=email,password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = "Access denied: wrong email or password."
                raise serializers.ValidationError(msg,code = "authorization")
            else:
                Token.objects.get_or_create(user=user)
        else:
            msg = "Both 'email' and 'password are required."
            raise serializers.ValidationError(msg, code="authorization")
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        # print(attrs)
        return attrs



    class Meta:
        model = User
        fields = ['email','password']

