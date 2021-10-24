from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import Textarea

from .models import Category, News, CommentNews
import re
from django.core.exceptions import ValidationError


# Этот класс отвечает за работу кнопки "Добавить новость".
# Данный класс позволит создать новость самостоятельно.
# Данная форма будет содержать пустые ячейки и всплывающее окно для выбора категории новости.
class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Выберите категорию"

    class Meta:
        model = News
        fields = ["title", "content", "is_published", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r'\d', title):
            raise ValidationError("Название не должно начинаться с цифры")
        return title


# Класс отвечает за регистрацию нового пользователя.
# Метод clean_email обеспечивает уникальность email, указываемого при регистрации
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Имя (необязательно поле)", required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повторить пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email


# Класс отвечает за вход пользователя в личный кабинет.
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Класс отвечает за самостоятельное изменения пароля авторизованного пользователя.
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Прежний пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Повторите новый пароль",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_messages = {
        'password_mismatch': 'Два поля пароля не совпадают.',
        'password_incorrect': "Старый пароль введён некоректно.",
    }


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentNews
        fields = ("comment",)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget = Textarea(attrs={'rows':4})
