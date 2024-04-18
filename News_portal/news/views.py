from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View)
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .tasks import send_email_task
from django.core.cache import cache


class PostsList(ListView):
    model = Post
    ordering = '-created_time'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице


class PostSearch(ListView):
    model = Post
    ordering = '-created_time'
    template_name = 'flatpages/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):

    permission_required = ('news.add_post',)

    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.post_type = 'Новость'
        send_email_task.delay(Post.pk)
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):

    permission_required = ('news.change_post',)

    model = Post
    fields = ['author', 'title', 'text']
    template_name = 'flatpages/news_edit.html'

    def dispatch(self, request, *args, **kwargs):
        Post = self.get_object()
        if Post.post_type != 'Новость':
            return redirect('articles_edit', Post.pk)
        return super(NewsUpdate, self).dispatch(request, *args, **kwargs)


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):

    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        Post = self.get_object()
        if Post.post_type != 'Новость':
            return redirect('articles_delete', Post.pk)
        return super(NewsDelete, self).dispatch(request, *args, **kwargs)


class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):

    permission_required = ('news.add_post',)

    form_class = PostForm
    model = Post
    template_name = 'flatpages/articles_create.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.post_type = 'Статья'
        send_email_task(Post.pk)
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):

    permission_required = ('news.change_post',)

    model = Post
    fields = ['author', 'title', 'text']
    template_name = 'flatpages/articles_edit.html'

    def dispatch(self, request, *args, **kwargs):
        Post = self.get_object()
        if Post.post_type != 'Статья':
            return redirect('news_edit', Post.pk)
        return super(ArticlesUpdate, self).dispatch(request, *args, **kwargs)


class ArticlesDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):

    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'flatpages/articles_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        Post = self.get_object()
        if Post.post_type != 'Статья':
            return redirect('news_delete', Post.pk)
        return super(ArticlesDelete, self).dispatch(request, *args, **kwargs)

class IndexView(View):
    def get(self, request):
        return render(request, 'flatpages/index.html')

class CategoryListView(PostsList):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-created_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
        context['categories'] = self.categories
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    categories = Category.objects.get(id=pk)
    categories.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'flatpages/subscribe.html',
                  {'categories': categories, 'message': message})


