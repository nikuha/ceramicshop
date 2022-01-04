from django.urls import path, include
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.UserLogoutView.as_view(), name='logout'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('edit/', authapp.ProfileUpdateView.as_view(), name='edit'),

    path('verify/<str:email>/<str:activate_key>/', authapp.UserRegisterView.verify, name='verify'),
]
