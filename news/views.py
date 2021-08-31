from django.shortcuts import render
from news.models import News, Category
from django.views.generic import ListView


# Создаю представлениe в виде класса, которое будет генерировать, имеющиеся в наличии новости.
# От самой свежей, до последней. Вне зависимости от её категории.
class HomeNews(ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context

# То же самое в виде функции...
# def index(request):
#     news = News.objects.all()
#     return render(request, "news/index.html", {"news": news,
#                                                "title": "Список новостей"})


# Вьюха в виде класса для вывода новостей по категориям.
class GiveCategories(ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GiveCategories, self).get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["id_category"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs["id_category"])

# Тоже самое ввиде функции
# def give_categories(request, id_category):
#     news = News.objects.filter(category_id=id_category)
#     category = Category.objects.get(pk=id_category)
#     return render(request, "news/category.html", {"news": news,
#                                                   "category": category})
