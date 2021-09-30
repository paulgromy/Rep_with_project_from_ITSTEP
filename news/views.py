from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from news.models import News, Category
from django.views.generic import ListView, FormView, DetailView, CreateView
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
class ViewNews(DetailView):
    model = News
    template_name = "news/view_news.html"
    context_object_name = "news_i"


#  Этот класс для формы, которая позволяет добавить новость в интерактивном режиме.
# Работа данной вьюхи отражена в forms.py
class Add_News(FormView):
    template_name = "news/add_news.html"
    form_class = NewsForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            News.objects.create(**form.cleaned_data)
            return redirect("Main")
        else:
            form = NewsForm()
        return render(request, self.template_name, {'form': form})


























