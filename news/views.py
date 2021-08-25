from django.shortcuts import render
from django.http import HttpResponse

from news.models import News, Category


# Создаю представление, которое будет генерировать, имеющиеся в наличии новости.
# И здесь же, прописываю путь к шаблону.
def index(request):
    news = News.objects.all()
    return render(request, "news/index.html", {"news": news,
                                               "title": "Список новостей"})

def give_categories(request, id_category):
    news = News.objects.filter(category_id = id_category)
    category = Category.objects.get(pk = id_category)
    return render(request, "news/category.html", {"news": news,
                                                  "category": category})


