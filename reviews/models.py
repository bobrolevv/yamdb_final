from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    role = models.CharField(
        'Роль', max_length=16, choices=ROLES, default='user')
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (self.role == 'admin' or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Genre(models.Model):
    name = models.CharField('Имя', max_length=256)
    slug = models.SlugField('Адрес', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    name = models.CharField('Имя', max_length=256)
    slug = models.SlugField('Адрес', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField('Имя', max_length=256)
    year = models.IntegerField('Год создания', validators=[
        MaxValueValidator(
            limit_value=int(dt.now().year),
            message='Слишком рано для него.'
        )
    ])
    description = models.TextField('Описание', default='')
    category = models.ForeignKey(
        Category, blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр')

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.CharField('Текст', max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор')
    score = models.IntegerField('Оценка произведения', validators=[
        MinValueValidator(
            limit_value=1,
            message='Не менее 1'
        ),
        MaxValueValidator(
            limit_value=10,
            message='Не более 10'
        )
    ])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    text = models.CharField('Текст', max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.review} - {self.author}'
