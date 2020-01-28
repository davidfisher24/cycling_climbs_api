# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.conf import settings
import jwt

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, max_length=255, unique=True)
    refresh_token = models.CharField(db_index=True, max_length=255, unique=True, null=True)
    reset_password_token = models.CharField(db_index=True, max_length=255, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        self._generate_refresh_token()
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def set_reset_password_token(self):
        return self._generate_password_refresh_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def _generate_refresh_token(self):
        dt = datetime.now()

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        self.refresh_token = token
        self.save()

    def _generate_password_refresh_token(self):
        dt = datetime.now() + timedelta(minutes=15)
        secret = self.password + self.created_at.strftime('%s')
        data = {
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }
        token = jwt.encode(data, secret, algorithm='HS256').decode('utf-8')
        self.reset_password_token = token
        self.save()
        return self.reset_password_token

    def verify_reset_token(self, token):
        secret = self.password + self.created_at.strftime('%s')
        data = jwt.decode(token, secret, algorithms='HS256')
        return data

    def set_new_password(self, new_password):
        self.set_password(new_password)
        self.reset_password_token = None
        self.save()
