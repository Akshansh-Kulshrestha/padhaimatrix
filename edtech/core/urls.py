from django.urls import path
from .views import *

urlpatterns = [
    path("article_list/", article_list, name="article_list"),
    path("add/", suggest_article, name="suggest_article"),
    path("<slug:slug>/", article_detail, name="article_detail"),
    path("<slug:slug>/edit/", suggest_correction, name="suggest_correction"),
    path('trending/', trending_articles, name='trending'),

]