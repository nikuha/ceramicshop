from django.urls import path, include
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('products/', adminapp.products, name='products'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('categories/restore/<int:pk>/', adminapp.category_restore, name='category_restore'),
    path('categories/', adminapp.categories, name='categories'),

    path('contacts/create/', adminapp.contact_create, name='contact_create'),
    path('contacts/update/<int:pk>/', adminapp.contact_update, name='contact_update'),
    path('contacts/delete/<int:pk>/', adminapp.contact_delete, name='contact_delete'),
    path('contacts/restore/<int:pk>/', adminapp.contact_restore, name='contact_restore'),
    path('contacts/', adminapp.contacts, name='contacts'),

    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('users/restore/<int:pk>/', adminapp.user_restore, name='user_restore'),
    path('users/', adminapp.users, name='users'),
]
