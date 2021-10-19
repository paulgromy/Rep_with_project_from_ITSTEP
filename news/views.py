from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from news.models import News, Category
from django.views.generic import ListView, FormView, DetailView, CreateView
from .forms import NewsForm, RegisterUserForm, LoginUserForm, MyPasswordChangeForm

# Создаю представлениe в виде класса, которое будет генерировать, имеющиеся в наличии новости.
# От самой свежей, до последней. Вне зависимости от её категории. Новость будет выводиться в формате:
# заголовок и первые несколько слов контента.
from .utils import DataMixin


class HomeNews(ListView):
    paginate_by = 3
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
class GiveCategories(ListView):
    paginate_by = 3
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
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


# Класс для самостоятельного изменения пароля пользователем. Будучи авторизованным.
# Использую class DataMixin из utils.py, что бы убрать дублируемый код.
class MyPasswordChangeView(DataMixin, PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'news/password_change.html'


# def password_reset_request(request):
#     if request.method == "POST":
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "main/password/password_reset_email.txt"
#                     c = {
#                         "email": user.email,
#                         'domain': '127.0.0.1:8000',
#                         'site_name': 'Website',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
#                     return redirect("/password_reset/done/")
#     password_reset_form = PasswordResetForm()
#     return render(request=request, template_name="news/password_reset.html",
#                   context={"password_reset_form": password_reset_form})
