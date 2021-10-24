from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path("", HomeNews.as_view(), name="Main"),
    path("category/<int:id_category>/", GiveCategories.as_view(), name="Category"),
    path("news/<int:pk>/", ViewNews.as_view(), name="view_news"),
    path("news/add-news/", Add_News.as_view(), name="add_news"),
    path("news/register/", RegisterUser.as_view(), name="register"),
    path("news/login/", LoginUser.as_view(), name="login"),
    path("news/logout/", LogoutUserView.as_view(), name="logout"),
    path('news/password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('news/password-reset/', views.PasswordResetView.as_view(template_name='news/password_reset.html'),
         name='password_reset'),
    path('news/password-reset/done/', views.PasswordResetDoneView.as_view(template_name='news/password_reset_done.html'),
         name='password_reset_done'),
    path('news/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='news/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('news/reset/done/', views.PasswordResetCompleteView.as_view(template_name='news/password_reset_complete.html'),
         name='password_reset_complete'),

]






