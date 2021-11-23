from django.urls import path, include
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('products/', include('mainapp.products.urls', namespace='products')),
]
