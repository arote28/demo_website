from django.urls import path      # re_path,include
from .views import UserRegistrationView,UserListView,UserDetailView,UserLoginView   # UserRegistrationView_tokenauth
# from rest_framework.authtoken import views
from rest_framework_simplejwt import views

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter(trailing_slash=False)
# router.register('auth', UserLoginView, basename='auth')

urlpatterns = [
    # re_path('^', include(router.urls)),

    path('register', UserRegistrationView.as_view(), name='register'),
    path('users_list', UserListView.as_view(), name='users_list'),
    path('user_details/<int:pk>/', UserDetailView.as_view(), name='user_details'),
    path('login', UserLoginView.as_view(), name='login'),
    # path('api-token-auth/', views.obtain_auth_token), #By exposing an api endpoint # to generte token directly by username and password
    # path('user_registartion__with_token/',UserRegistrationView_tokenauth.as_view(), name='user_registartion__with_token') # genrerate token at the time of registration
    path('jwttoken', views.TokenObtainPairView.as_view(), name='token_obtain_pair'), #jwt endpoint to generate access token and refresh token
    path('jwttoken/refresh', views.TokenRefreshView.as_view(), name='token_refresh'), # jwt endpoint to get new access token by providing refresh token
]


# from rest_framework.routers import DefaultRoutera

# router = DefaultRouter()
# router.register(r'users', UsersViewset,basename='user')
# router.register(r'user_types', User_types_view,basename='user_types')
# urlpatterns = [
#     path('UserRegistration', Basic_Auth_User_Registration.as_view()),
#     path('UserLogin', Basic_Auth_User_LoginDetailView.as_view()),
#     re_path('^', include(router.urls))
# ]

