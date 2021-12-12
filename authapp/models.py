from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(verbose_name='аватарка', upload_to='user_avatars', blank=True)

    @property
    def image_or_default(self):
        return self.avatar.url if self.avatar else static('img/default.png')

