from django.db import models
from django.contrib.auth.models import User  

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile:
            raise ValueError('Users must have a mobile number')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None):
        user = self.create_user(
            email,
            name=name,
            mobile=mobile,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email


class Expense(models.Model):
    SPLIT_METHODS = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENTAGE', 'Percentage'),
    ]
    title = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHODS)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    participants = models.ManyToManyField(User, related_name='expenses')

class Split(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='splits')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
