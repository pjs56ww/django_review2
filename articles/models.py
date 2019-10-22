from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from django.conf import settings

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    content2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # article.user => article 입장에서
    # comment.article
    # article.comment_set.all()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')  # models.py 에서만 이렇게 가져오고 나머지는 form.py 문법을 통해 가져온다. => django 실행 순서와 관련있다.

    class Meta:
        ordering = ('-pk', )

class Person(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(
        max_length=100,
        validators=[EmailValidator(message='이메일 형식에 맞지 않습니다.')]

    )
    age = models.IntegerField(
        validators=[MinValueValidator(19, message='미성년자는 노노')]
    )


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    

    class Meta:
        ordering = ('-pk', )