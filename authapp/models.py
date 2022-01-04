import hashlib
import random

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(verbose_name='аватарка', upload_to='user_avatars', blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def set_activation_key(self):
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()

    def is_activation_key_expired(self):
        return self.activation_key_expires + timedelta(hours=48) < now()

    def send_verify_link(self):
        verify_link = reverse('authapp:verify', args=[self.email, self.activation_key])
        subject = f'Для активации учетной записи {self.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {self.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        self.email_user(subject, message, settings.EMAIL_HOST_USER, fail_silently=False)
        return True

    def check_activation_key(self, activate_key):
        if self and self.activation_key == activate_key and not self.is_activation_key_expired():
            self.activation_key = ''
            self.activation_key_expires = None
            self.is_active = True
            self.save()
            return True
        else:
            return False

    @property
    def image_or_default(self):
        return self.avatar.url if self.avatar else static('img/default.png')

    @property
    def first_or_user_name(self):
        return self.first_name if self.first_name else self.username


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='о себе', blank=True, null=True)
    gender = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=1)
    languages = models.CharField(verbose_name='язык', blank=True, null=True, max_length=10)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.userprofile.save()
