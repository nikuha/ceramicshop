from django.urls import path, include
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.add_product, name='add'),
    path('remove/<int:pk>)/', basketapp.remove_product, name='remove'),

]
