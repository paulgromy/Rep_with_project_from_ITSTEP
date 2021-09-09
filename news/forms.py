from django import forms
from .models import Category


# Этот класс отвечает за работу кнопки "Добавить новость".
# Данный класс позволит создать новость самостоятельно.
# Данная форма будет содержать пустые ячейки и всплывающее окно для выбора категории новости.
class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label="Название",
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="Текст", required=False,
                              widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
    is_published = forms.BooleanField(label="Опубликовано", initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория",
                                      empty_label="Выбрать категорию",
                                      widget=forms.Select(attrs={"class": "form-control"}))


# class NewsForm(forms.ModelForm):
#     class Meta:
#         model = News
#         fields = ["title", "content", "is_published", "category"]
#         widgets = {
#             "title": forms.TextInput(attrs={"class": "form-control"}),
#             "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
#             "category": forms.Select(attrs={"class": "form-control"}),
#         }
