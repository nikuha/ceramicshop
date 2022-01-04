from django.urls import path, include
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.IndexView.as_view(), name='index'),

    path('products/create/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/', adminapp.ProductListView.as_view(), name='category_products'),
    path('products/', adminapp.ProductListView.as_view(), name='products'),
    path('products/toggle_active/<int:pk>/', adminapp.ProductToggleActiveView.as_view(), name='product_toggle_active'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('categories/toggle_active/<int:pk>/', adminapp.CategoryToggleActiveView.as_view(), name='category_toggle_active'),

    path('contacts/create/', adminapp.ContactCreateView.as_view(), name='contact_create'),
    path('contacts/update/<int:pk>/', adminapp.ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/', adminapp.ContactListView.as_view(), name='contacts'),
    path('contacts/toggle_active/<int:pk>/', adminapp.ContactToggleActiveView.as_view(), name='contact_toggle_active'),

    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('users/', adminapp.UserListView.as_view(), name='users'),
    path('users/toggle_active/<int:pk>/', adminapp.UserToggleActiveView.as_view(), name='user_toggle_active'),
]
