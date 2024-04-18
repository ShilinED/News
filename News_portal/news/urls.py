from django.urls import path
# Импортируем созданные нами представления
from .views import (
    PostsList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, PostSearch,
    ArticlesCreate, ArticlesUpdate, ArticlesDelete, CategoryListView, subscribe
)

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60 * 1)(PostsList.as_view()), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', cache_page(60 * 5)(PostSearch.as_view()), name='post_search'),

    path('news/create/', cache_page(60 * 5)(NewsCreate.as_view()), name='news_create'),
    path('news/<int:pk>/edit/', cache_page(60 * 5)(NewsUpdate.as_view()), name='news_edit'),
    path('news/<int:pk>/delete/', cache_page(60 * 5)(NewsDelete.as_view()), name='news_delete'),

    path('articles/create/', cache_page(60 * 5)(ArticlesCreate.as_view()), name='articles_create'),
    path('articles/<int:pk>/edit/', cache_page(60 * 5)(ArticlesUpdate.as_view()), name='articles_edit'),
    path('articles/<int:pk>/delete/', cache_page(60 * 5)(ArticlesDelete.as_view()), name='articles_delete'),

    path('categories/<int:pk>', cache_page(60 * 5)(CategoryListView.as_view()), name='category_list'),
    path('categories/<int:pk>/subscribe', cache_page(60 * 5)(subscribe), name='subscribe'),
]