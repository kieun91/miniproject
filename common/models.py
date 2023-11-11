from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=255, null=True, default='<유저#123>')
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=('groups'),
                                    help_text=(
                                        '닉네임을 입력하세요.'))
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True,
                                              verbose_name=('user permissions'),
                                              help_text=('Specific permissions for this user.'))
    def __str__(self):
        return self.username