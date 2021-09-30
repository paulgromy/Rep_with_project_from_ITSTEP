from django.db import models
from django.urls import reverse_lazy


# Класс для публикации новостей. Описание полей.
# Основная модель, которая формирует формат и наполнение новости.
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=150, verbose_name="Фото", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, verbose_name="Категория")

    # Формирует уникальный адрес для каждого экземпляра модели.
    def get_absolute_url(self):
        return reverse_lazy("view_news", kwargs={"pk": self.pk})

    # Метод для отображения строкового представления.
    def __str__(self):
        return self.title

    # Класс для дополнительных настроек в админке.
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]


# Класс для определения новостей по категориям. Является вспомогательным.
# Содержит связь один-ко-многим по отношению к class News, т.е. к одной категории
# может принадлежать несколько новостей.
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Наименование категории")

    def get_absolute_url(self):
        return reverse_lazy("Category", kwargs={"id_category": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]
