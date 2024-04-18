from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=5)

    class Meta:
        model = Post
        fields = ['author', 'categories', 'title', 'text',]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if text == title:
            raise ValidationError(
                "Содержание не должно быть идентично названию."
            )

        return cleaned_data