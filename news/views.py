from django.shortcuts import render, get_object_or_404
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


# Вьюха  для вывода новостей по категориям.
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


# Вьюха для чтения конкретной новости.
class ViewNews(ListView):
    model = News
    template_name = "news/view_news.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewNews, self).get_context_data(**kwargs)
        context["news_i"] = get_object_or_404(News, pk = self.kwargs["news_id"])
        return context
















