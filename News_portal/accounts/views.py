from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/complete_signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        return context


class QuitView(TemplateView):
    template_name = 'flatpages/logout.html'


class AuthorView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/author_status.html'


@login_required
def get_author_status(request):

    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)

    return redirect('http://127.0.0.1:8000/auth/author_view/')