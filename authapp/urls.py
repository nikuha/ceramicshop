from django.urls import path, include
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.RegisterShopUserView.as_view(), name='register'),
    path('edit/', authapp.edit, name='edit'),

    path('verify/<str:email>/<str:activate_key>/', authapp.RegisterShopUserView.verify, name='verify'),
]
