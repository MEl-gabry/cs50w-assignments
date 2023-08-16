from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.new, name="newpage"),
    path("editpage/<str:title>", views.edit, name="editpage"),
    path("randompage", views.random, name="randompage"),
    path("<str:title>", views.entry, name="entry")
]
