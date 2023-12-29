# Импортируем необходимые модули: модели Django и встроенную модель пользователя User.
from django.db import models
from django.contrib.auth.models import User

# Определяем модель Author для хранения информации об авторах.
class Author(models.Model):
    # Связь один к одному с моделью User. Каждый автор ассоциирован с одним пользователем.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Целочисленное поле для хранения рейтинга автора.
    rating = models.IntegerField(default=0)

    # Метод для обновления рейтинга автора.
    def update_rating(self):
        # Рассчитываем рейтинг как сумму рейтингов всех постов автора, умноженных на 3,
        # плюс сумму рейтингов всех комментариев пользователя,
        # плюс сумму рейтингов всех комментариев к постам автора.
        self.rating = sum([post.rating * 3 for post in Post.objects.filter(author=self)]) + \
                      sum([comment.rating for comment in Comment.objects.filter(user=self.user)]) + \
                      sum([comment.rating for comment in Comment.objects.filter(post__author=self)])
        # Сохраняем обновленный рейтинг.
        self.save()

# Определяем модель Category для хранения категорий постов.
class Category(models.Model):
    # Строковое поле для названия категории, каждое название должно быть уникальным.
    name = models.CharField(max_length=100, unique=True)

# Определяем модель Post для хранения постов (статей или новостей).
class Post(models.Model):
    # Связь многие к одному с моделью Author.
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Константы и выбор для типа поста: статья или новость.
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
    ]
    # Строковое поле для типа поста с предопределенными выборами.
    type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    # Поле даты и времени для автоматической установки времени создания поста.
    creation_date = models.DateTimeField(auto_now_add=True)
    # Связь многие ко многим с моделью Category через промежуточную модель PostCategory.
    categories = models.ManyToManyField(Category, through='PostCategory')
    # Поля для заголовка и текста поста.
    title = models.CharField(max_length=100)
    text = models.TextField()
    # Целочисленное поле для рейтинга поста.
    rating = models.IntegerField(default=0)

    # Методы для увеличения и уменьшения рейтинга поста.
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод для предварительного просмотра текста поста (первые 124 символа плюс многоточие).
    def preview(self):
        return self.text[:124] + '...'

# Промежуточная модель PostCategory для связи многие ко многим между Post и Category.
class PostCategory(models.Model):
    # Связь многие к одному с моделью Post и Category.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Определяем модель Comment для хранения комментариев к постам.
class Comment(models.Model):
    # Связь многие к одному с моделями Post и User.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Поле для текста комментария и автоматической установки времени создания комментария.
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    # Целочисленное поле для рейтинга комментария.
    rating = models.IntegerField(default=0)

    # Методы для увеличения и уменьшения рейтинга комментария.
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


