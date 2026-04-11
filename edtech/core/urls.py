from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("tutorials/", article_list, name="article_list"),
    path("ask/", ask, name="ask"),
    path("add/", suggest_article, name="suggest_article"),
    path("tutorials/<slug:subject_slug>/<slug:topic_slug>/", article_detail, name="article_detail"),
    path("notes/", notes_page, name="notes_page"),
    path("software/", software_list, name="software_list"),
]