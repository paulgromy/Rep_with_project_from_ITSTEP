from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeNews.as_view(), name="Main"),
    path("category/<int:id_category>/", GiveCategories.as_view(), name="Category"),
    path("news/<int:news_id>/", ViewNews.as_view(), name="view_news"),
    path("news/add-news/", add_news, name="add_news"),
]
