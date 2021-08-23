from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("news.urls")),

]

# Условие для работы с медиафайлами. Да, это требуется только для локального сервера,
# но пока что я с ним и работаю.
# В settings.py прописаны дополнительные переменные MEDIA_ROOT и MEDIA_URL.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
