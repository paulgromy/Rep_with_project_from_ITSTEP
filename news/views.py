from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from news.models import News, Category, CommentNews
from django.views.generic import ListView, FormView, DetailView, CreateView, RedirectView
from .forms import NewsForm, RegisterUserForm, LoginUserForm, MyPasswordChangeForm, CommentForm
from .utils import DataMixin


# Создаю представлениe в виде класса, которое будет генерировать, имеющиеся в наличии новости.
# От самой свежей, до последней. Вне зависимости от её категории. Новость будет выводиться в формате:
# заголовок и первые несколько слов контента.
class HomeNews(DataMixin, ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# Вьюха  для вывода новостей по категориям. Пользователь на главной странице, сможет выбрать из меню
# интерисующую категорию новостей.
class GiveCategories(DataMixin, ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GiveCategories, self).get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["id_category"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs["id_category"]).select_related('category')


# Вьюха для чтения конкретной новости. Пользователь, нажимаю на кнопку "Читать далее",
# сможет ознакомиться с новостью полностью.
class ViewNews(FormMixin, DetailView):
    model = News
    template_name = "news/view_news.html"
    context_object_name = "news"
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('view_news', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.news = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


#  Этот класс для формы, которая позволяет добавить новость в интерактивном режиме.
# Работа данной вьюхи отражена в forms.py
class Add_News(LoginRequiredMixin, FormView):
    template_name = "news/add_news.html"
    form_class = NewsForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            News.objects.create(**form.cleaned_data)
            return redirect("Main")
        else:
            form = NewsForm()
        return render(request, self.template_name, {'form': form})


# Класс, отвечающий за регистрацию новых пользователей на сайте.
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('Main')


# Класс, отвечающий за авторизацию пользователя на сайте.
# Использую class DataMixin из utils.py, что бы убрать дублируемый код.
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'


# Выход пользователя из личного кабинета
class LogoutUserView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


# Класс для самостоятельного изменения пароля пользователем. Будучи авторизованным.
# Использую class DataMixin из utils.py, что бы убрать дублируемый код.
class MyPasswordChangeView(LoginRequiredMixin, DataMixin, PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'news/password_change.html'
