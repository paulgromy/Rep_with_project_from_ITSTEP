from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeNews.as_view(), name="Main"),
    path("category/<int:id_category>/", GiveCategories.as_view(), name="Category"),

]
