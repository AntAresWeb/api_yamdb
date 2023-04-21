from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHIOCE_ROLE = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    REQUIRED_FIELDS = ["email", "password"]
    role = models.CharField(verbose_name='Роль пользователя', max_length=16,
                            choices=CHIOCE_ROLE, default='user')
    bio = models.TextField(verbose_name='Биография', blank=True)
    confirmation_code = models.CharField(verbose_name='Код подтверждения',
                                         max_length=40, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роль пользователей'
        ordering = ('-id',)
