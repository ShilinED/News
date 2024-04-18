from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    date = DateFilter(field_name="created_time",
                      widget=forms.DateInput(attrs={'type': "date"}),
                      label='Дата',
                      lookup_expr='date__gte')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }