from django.contrib.auth.models import AbstractUser
from django.db import models

class RoleUser(AbstractUser):
    CHIOCE_ROLE = (
        ('U', 'User'),
        ('M', 'Moderator'),
        ('A', 'Admin'),
    )
    role = models.CharField(verbose_name='Пользовательская роль',
                            max_length=1, choices=CHIOCE_ROLE, default='U')
    bio = models.TextField(verbose_name='Биография', blank=True,
                           max_length=250)

    def __str__(self):
        return self.username
