from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
from datetime import timedelta

from django.utils.timezone import now


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(verbose_name='аватарка', upload_to='user_avatars', blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def is_activation_key_expired(self):
        return self.activation_key_expires + timedelta(hours=48) < now()

    @property
    def image_or_default(self):
        return self.avatar.url if self.avatar else static('img/default.png')

