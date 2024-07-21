from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from rest_framework import serializers

from users.models import User

"""
    The authentication class of user login is defined to realize multi-field login
"""


class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            print(user)
        except:
            raise serializers.ValidationError({
                "error": "user not exist"
            })
        else:
            if user.check_password(password):
                print(1111)
                return user
            else:
                raise serializers.ValidationError({'error': 'Invalid Password'})
