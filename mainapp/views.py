import json

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
    # создание json файла
    # sections = [
    #     {'name': 'Чайные чашки'},
    #     {'name': 'Кофейные чашки'},
    #     {'name': 'Блюда'},
    #     {'name': 'Наборы'},
    #     {'name': 'Для ванной'},
    # ]
    # items = [
    #     {'name': 'Пиала для меда', 'img': static('img/01.jpg')},
    #     {'name': 'Чашечка для меда', 'img': static('img/02.jpg')},
    #     {'name': 'Чашка для варенья', 'img': static('img/03.jpg')},
    #     {'name': 'Набор мисок', 'img': static('img/04.jpg')},
    #     {'name': 'Салатница "Рыба"', 'img': static('img/05.jpg')},
    #     {'name': 'Салатница "Осень"', 'img': static('img/06.jpg')}
    # ]
    # with open('mainapp/data/sections.json', 'w') as f:
    #     f.write(json.dumps(sections))
    # with open('mainapp/data/products.json', 'w') as f:
    #     f.write(json.dumps(items))

    # чтение из json файла
    with open('mainapp/data/sections.json') as json_file:
        sections = json.load(json_file)
    with open('mainapp/data/products.json') as json_file:
        items = json.load(json_file)

    context = {
        'page_title': 'посуда',
        'sections': sections,
        'products': items
    }
    return render(request, 'mainapp/products.html', context)


def contacts(request):
    items = [
        {'city': 'Сочи', 'phone': '+7 (918) 555-55-55', 'email': 'sochi@ceramicsochi.com'},
        {'city': 'Красная Поляна', 'phone': '+7 (918) 777-77-77', 'email': 'polyana@ceramicsochi.com'},
        {'city': 'Адлер', 'phone': '+7 (918) 888-88-88', 'email': 'adler@ceramicsochi.com'},
    ]
    context = {
        'page_title': 'контакты',
        'contacts': items
    }
    return render(request, 'mainapp/contacts.html', context)
