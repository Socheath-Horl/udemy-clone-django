from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models

from courses.models import Course


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password, name, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Supperuser must have is_staff True')

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser True')

        return self.create_user(email, password, name, **kwargs)

    def create_user(self, email, password, name, **kwargs):
        if not email:
            raise ValueError('You must provide a valid email')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **kwargs)

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    paid_courses = models.ManyToManyField(Course)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.name} {self.email}'

    def get_all_courses(self):
        courses = []
        for course in self.paid_courses.all():
            courses.append(course.course_uuid)
        return courses
