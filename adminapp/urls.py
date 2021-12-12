from django.urls import path, include
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('categories/', adminapp.categories, name='categories'),
    path('products/', adminapp.products, name='products'),
    path('contacts/', adminapp.contacts, name='contacts'),

    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('users/restore/<int:pk>/', adminapp.user_restore, name='user_restore'),
    path('users/', adminapp.users, name='users'),
]
