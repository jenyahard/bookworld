from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    userdata = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    verbose_name='Аккаунт автора',
                                    )
    author_name = models.CharField(
        max_length=256,
        verbose_name='Имя автора книги',
    )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self) -> str:
        return self.author_name


class Book(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название книги',
    )
    text = models.TextField(
        verbose_name='Описание книги',
    )
    author = models.ManyToManyField(Author,
                                    related_name='author',
                                    verbose_name='Автор книги',
                                    )
    image = models.ImageField('Изображение',
                              upload_to='book_images',
                              blank=True,
                              )
    is_archived = models.BooleanField(
        default=False,
        verbose_name='В архиве',
        help_text='Поставь галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE
                               )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
