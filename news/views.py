from django.shortcuts import render
from django.http import HttpResponse

from news.models import News, Category


# Создаю представление, которое будет генерировать, имеющиеся в наличии новости.
# И здесь же, прописываю путь к шаблону.
def index(request):
    news = News.objects.all()
    categories = Category.objects.order_by()
    return render(request, "news/index.html", {"news": news,
                                               "title": "Список новостей",
                                               "categories": categories,})



def give_categories(request, id_category):
    news = News.objects.filter(category_id = id_category)
    categories = Category.objects.all()
    category = Category.objects.get(pk = id_category)
    return render(request, "news/category.html", {"news": news,
                                                  "categories": categories,
                                                  "category": category})


