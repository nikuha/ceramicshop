from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden
from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'personal', 'photo_200',
                                                                 'first_name', 'last_name')),
                                                access_token=response['access_token'], v=5.131)), None))

    data_response = requests.get(api_url)
    if data_response.ok:
        data = data_response.json()['response'][0]

        if data['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMALE
        elif data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE
        else:
            pass

        if data['about']:
            user.userprofile.about = data['about']

        user.first_name = data['first_name']
        user.last_name = data['last_name']

        birthdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        today = timezone.now().date()
        one_or_zero = int((today.month, today.day) < (birthdate.month, birthdate.day))
        year_difference = today.year - birthdate.year
        age = year_difference - one_or_zero

        user.age = age

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if data['photo_200']:
            photo_link = data['photo_200']
            photo_response = requests.get(photo_link)
            path_photo = f'{user.avatar.field.upload_to}/{user.pk}.jpg'
            with open(f'{settings.MEDIA_ROOT}/{path_photo}', 'wb') as photo:
                photo.write(photo_response.content)
            user.avatar = path_photo

        if data['personal']['langs']:
            user.userprofile.languages = data['personal']['langs'][0] if len(data['personal']['langs'][0]) > 0 else 'EN'
        user.save()
