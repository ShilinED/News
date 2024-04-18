from django.urls import path
from .views import IndexView, QuitView, AuthorView, get_author_status

urlpatterns = [
    path('complete/', IndexView.as_view()),
    path('quit/', QuitView.as_view()),
    path('upgrade/', get_author_status, name='upgrade'),
    path('author_view/', AuthorView.as_view()),
]