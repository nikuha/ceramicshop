from django.urls import path, include
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),

    path('products/create/<int:pk>/', adminapp.product_create, name='product_create'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/toggle_active/<int:pk>/', adminapp.product_toggle_active, name='product_toggle_active'),
    path('products/<int:pk>/', adminapp.products, name='category_products'),
    path('products/', adminapp.products, name='products'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('categories/toggle_active/<int:pk>/', adminapp.category_toggle_active, name='category_toggle_active'),

    path('contacts/create/', adminapp.contact_create, name='contact_create'),
    path('contacts/update/<int:pk>/', adminapp.contact_update, name='contact_update'),
    path('contacts/toggle_active/<int:pk>/', adminapp.contact_toggle_active, name='contact_toggle_active'),
    path('contacts/', adminapp.contacts, name='contacts'),

    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/toggle_active/<int:pk>/', adminapp.user_toggle_active, name='user_toggle_active'),
    path('users/', adminapp.users, name='users'),
]
