from django.urls import path
import mainapp.views as mainapp

app_name = 'products'

urlpatterns = [
    path('', mainapp.HotProductsView.as_view(), name='index'),
    path('all/', mainapp.AllProductsView.as_view(), name='all'),
    path('category_<int:pk>/', mainapp.ProductsView.as_view(), name='category'),
    path('<int:pk>/', mainapp.ProductView.as_view(), name='product')
]
