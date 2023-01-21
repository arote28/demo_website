from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from .serializers import UserRegistrationSerializer,UserDetailSerializer,UserLoginSerializer
# from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views
# from rest_framework.authtoken.views import ObtainAuthToken

from .models import User
from django.contrib.auth import authenticate,login
from django.core.exceptions import ImproperlyConfigured
# from django.utils.timezone import now

# Create your views here.
def get_noncustomers_login(email):
    user = User.objects.get(email = email)
    if user.is_staff == True and user.is_active == True :
        return True
    else:
        return False

def check_valid_uer_for_basicauthentication(instance,queryset):
    if instance.id == queryset.pk:
        # import pdb;
        # pdb.set_trace()
        return True
    else:
        raise exceptions.AuthenticationFailed('Enter valid details')

def get_authenticated_user(email,password):
    user = authenticate(username=email,password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user

# user registration with generating token
# class UserRegistrationView_tokenauth(APIView):
#
#     serializer_class = UserRegistrationSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#
#         serializer = self.serializer_class(data=request.data)
#         valid = serializer.is_valid(raise_exception=True)
#
#         if valid:
#             user = serializer.save()
#             # import pdb;
#             # pdb.set_trace()
#             # user = serializer.validated_data['email']
#             token, created = Token.objects.get_or_create(user=user)
#             status_code = status.HTTP_201_CREATED
#             response = {
#                 "success":True,
#                 "status_code":status_code,
#                 "message": "User Registered Successfully",
#                 'token': token.key,
#                 "user": serializer.data
#             }
#             return Response(response, status=status_code)
#         # import pdb;
#         # pdb.set_trace()
#         # serializer = self.serializer_class(data = request.data)
#         # serializer.is_valid(raise_exception=True)
#         # user = serializer.validated_data['user']
#         # token,created = Token.objects.get_or_create(user=user)
#         # return Response({
#         #     'email':user.email,
#         #     'user_id':user.pk,
#         #     'token':token.key
#         # })

# user registration without generating token
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                "success":True,
                "status_code":status_code,
                "message": "User Registered Successfully",
                "user": serializer.data
            }
            return Response(response, status=status_code)

# user login with generating JWT authentication
class UserLoginView(APIView):
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserLoginSerializer

    def post(self,request):

        serializer = self.serializer_class(data = request.data)
        user = get_authenticated_user(email=request.data['email'], password=request.data['password'])

        # import pdb;
        # pdb.set_trace()
        valid = serializer.is_valid()
        if valid and user is not None and user.is_active:

        # if user is not None:
        #     if user.is_active:
        #         login(request,user)
            # user = serializer.validated_data['email']
            login(request, user)
            # user = serializer.validated_data['email']
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            status_code = status.HTTP_200_OK
            response = {
                "success": True,
                "status_code": status_code,
                "message": "User logged in successfully",
                "user":serializer.data,
                # "token":token
                # "authenticatedUser":{
                #     "email":serializer.data['email'],
                    # "role":serializer.data['role']
                # }
            }
            return Response(response,status=status_code)
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                "message": "Unauthenticated user.",
            }
            return Response(response, status=status_code)
# basic authentication for user login without creating token
# class UserLoginView(viewsets.GenericViewSet):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [AllowAny]
#     serializer_class = EmptySerializer
#     serializer_classes = {
#         'login':UserAuthSerializer
#     }
#
#     @action(methods=['POST',], detail=False)
#     def login(self,request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         import pdb;
#         pdb.set_trace()
#         user = get_authenticated_user(email= request.data['email'],password=request.data['password'])
#         data = UserAuthSerializer(user).data
#         return Response(data=data,status=status.HTTP_200_OK)
#
#     def get_serializer_class(self):
#         if not isinstance(self.serializer_classes, dict):
#             raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
#
#         if self.action in self.serializer_classes.keys():
#             return self.serializer_classes[self.action]
#         return super().get_serializer_class()

#user login with generate token
# class UserLoginView(APIView):
#     # authentication_classes = [BasicAuthentication]
#     permission_classes = [AllowAny]
#     serializer_class = UserLoginSerializer
#
#     def post(self,request):
#
#         serializer = self.serializer_class(data = request.data)
#         user = get_authenticated_user(email=request.data['email'], password=request.data['password'])
#
#         # import pdb;
#         # pdb.set_trace()
#         valid = serializer.is_valid()
#         if valid and user is not None and user.is_active:
#
#         # if user is not None:
#         #     if user.is_active:
#         #         login(request,user)
#             # user = serializer.validated_data['email']
#             login(request, user)
#             # user = serializer.validated_data['email']
#             token, created = Token.objects.get_or_create(user=user)
#             print(token)
#             status_code = status.HTTP_200_OK
#             response = {
#                 "success": True,
#                 "status_code": status_code,
#                 "message": "User logged in successfully",
#                 "user":serializer.data,
#                 # "token":token
#                 # "authenticatedUser":{
#                 #     "email":serializer.data['email'],
#                     # "role":serializer.data['role']
#                 # }
#             }
#             return Response(response,status=status_code)
#         else:
#             status_code = status.HTTP_401_UNAUTHORIZED
#             response = {
#                 "message": "Unauthenticated user.",
#             }
#             return Response(response, status=status_code)


class UserListView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.get(email = request.user.email)

        if user.is_superuser:

            queryset = User.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            status_code = status.HTTP_200_OK
            response = {
                "success":True,
                "status_code":status_code,
                "message":"Successfully fetched all users",
                "List":serializer.data
            }
            return Response(response, status=status_code)

# class UserDetailView_for_tokenauth(APIView):
#     serializer_class =

class UserDetailView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):

        queryset = self.request.user
        instance = self.get_object()
        # serializer = self.get_serializer(instance)
        authentication = check_valid_uer_for_basicauthentication(instance,queryset)
        if authentication:
            serializer = self.serializer_class(self.request.user, many=False)
            return Response(serializer.data)
    #
    def put(self, request, *args, **kwargs):
        # import pdb;
        # pdb.set_trace()
        queryset = self.request.user
        instance = self.get_object()
        serializer = self.serializer_class(instance,data = request.data, many=False)
        # serializer = self.serializer_class(data=request.data)
        # valid = serializer.is_valid()

        # if valid:
        authentication = check_valid_uer_for_basicauthentication(instance,queryset)
        if authentication and serializer.is_valid():
            serializer.save()
            # serializer = self.serializer_class(queryset, many=True)
            status_code = status.HTTP_200_OK
            response = {
                "success":True,
                "status_code":status_code,
                "message":"Successfully update user details",
                "User_Details":serializer.data
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


