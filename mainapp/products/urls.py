from django.urls import path
import mainapp.views as mainapp

app_name = 'products'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('category_<int:pk>/', mainapp.products, name='category'),
    path('<int:pk>/', mainapp.product, name='product')
]
