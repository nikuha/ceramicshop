from django.urls import path

from ordersapp.views import OrderListView, OrderCreateView, OrderDeleteView, OrderDetailView, OrderUpdateView, \
                            order_forming_complete, get_product_price, create_from_basket

app_name = 'ordersapp'
urlpatterns = [

    path('', OrderListView.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetailView.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),
    path('get_product_price/<int:pk>/', get_product_price, name='get_product_price'),
    path('create_from_basket/', create_from_basket, name='create_from_basket'),

]
