from django.shortcuts import render
from django.templatetags.static import static


# Create your views here.
def index(request):
    context = {
        'page_title': 'главная',
        'content_class': 'main-page'
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    sections = [
        {'name': 'Чайные чашки'},
        {'name': 'Кофейные чашки'},
        {'name': 'Блюда'},
        {'name': 'Наборы'},
        {'name': 'Для ванной'},
    ]
    items = [
        {'name': 'Пиала для меда', 'img': static('img/01.jpg')},
        {'name': 'Чашечка для меда', 'img': static('img/02.jpg')},
        {'name': 'Чашка для варенья', 'img': static('img/03.jpg')},
        {'name': 'Набор мисок', 'img': static('img/04.jpg')},
        {'name': 'Салатница "Рыба"', 'img': static('img/05.jpg')},
        {'name': 'Салатница "Осень"', 'img': static('img/06.jpg')}
    ]
    context = {
        'page_title': 'посуда',
        'sections': sections,
        'products': items
    }
    return render(request, 'mainapp/products.html', context)


def contacts(request):
    context = {
        'page_title': 'контакты'
    }
    return render(request, 'mainapp/contacts.html', context)
