from django.shortcuts import render, get_object_or_404, redirect
from news.models import News, Category
from django.views.generic import ListView
from .forms import NewsForm


# Создаю представлениe в виде класса, которое будет генерировать, имеющиеся в наличии новости.
# От самой свежей, до последней. Вне зависимости от её категории. Новость будет выводиться в формате:
# заголовок и первые несколько слов контента.
class HomeNews(ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


# Вьюха  для вывода новостей по категориям. Пользователь на главной странице, сможет выбрать из меню
# интерисующую категорию новостей.
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


# Вьюха для чтения конкретной новости. Пользователь, нажимаю на кнопку "Читать далее",
# сможет ознакомиться с новостью полностью.
class ViewNews(ListView):
    model = News
    template_name = "news/view_news.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewNews, self).get_context_data(**kwargs)
        context["news_i"] = get_object_or_404(News, pk=self.kwargs["news_id"])
        return context


#  Этот класс для формы, которая позволяет добавить новость в интерактивном режиме.
# Работа данной вьюхи отражена в forms.py
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = News.objects.create(**form.cleaned_data)
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, "news/add_news.html", {"form": form})
