from django import forms
from .models import Category, News
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


