from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Category, CommentNews


# Создаю класс для настройки админки.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at", "update_at", "is_published", 'get_photo')
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category")
    fields = ("title", "category",'content', "created_at", "update_at", "is_published", 'get_photo','photo', 'views')
    readonly_fields = ("created_at", "update_at", 'views', 'get_photo')
    save_on_top = True

    @admin.display(empty_value='-//-//-//-')
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src = "{obj.photo.url}" width = "50" height = "30">')
    get_photo.short_description = 'Фото'


# Дополнительный класс категоризации новостей, так же для настроек в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)


@admin.register(CommentNews)
class CommentNewsAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id", "user")


admin.site.site_title = "Управление"
admin.site.site_header = "Управление сайтом"
