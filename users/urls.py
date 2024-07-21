from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import Login, Register, UserDetails, AddrView,SendSMSView

urlpatterns = [
    # login
    path('login/', Login.as_view()),
    # register
    path('register/', Register.as_view()),
    # refresh token
    path('token/refresh/', TokenRefreshView.as_view()),
    # verify token
    path('token/verify/', TokenVerifyView.as_view()),
    # query single user information
    path('users/<int:pk>/', UserDetails.as_view({'get': "retrieve"})),
    # upload user's avatar
    path('<int:pk>/avatar/upload/', UserDetails.as_view({'post': "upload_avatar"})),

    # add address and list of addresses
    path('address/', AddrView.as_view({
        "post": "create",
        "get": "list"
    })),
    path('address/<int:pk>/', AddrView.as_view({
        "delete": "destroy",
        "put": "update"
    })),
    path('address/<int:pk>/default/',AddrView.as_view({
        "put":"set_default_addr"
    })),
    path('sendsms/',SendSMSView.as_view())
]
