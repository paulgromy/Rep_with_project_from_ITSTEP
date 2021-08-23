from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name = "Main"),
    path("category/<int:id_category>/", give_categories, name = "Category"),

]