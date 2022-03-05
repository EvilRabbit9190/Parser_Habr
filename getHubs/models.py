from pyexpat import model
from django.db import models


class Hubs(models.Model):
    header = models.CharField(max_length=200, verbose_name="Заголовок")
    date = models.DateField(null='2022-03-03', verbose_name="Дата публикации")
    link_post = models.URLField(max_length=100, verbose_name="Ссылка на пост")
    author_name = models.CharField(max_length=50, verbose_name="Имя автора")
    author_link = models.URLField(max_length=100, verbose_name="Ссылка на автора")
    post_id = models.PositiveIntegerField(verbose_name="ID поста")
    content = models.TextField(verbose_name="Контент")

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return str(self.pk)
