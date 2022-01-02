from django.urls import path, include
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.IndexView.as_view(), name='index'),
    path('contacts/', mainapp.ContactsView.as_view(), name='contacts'),
    path('products/', include('mainapp.products.urls', namespace='products')),
]
