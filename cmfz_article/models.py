from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    cate = models.BooleanField()

    class Meta:
        db_table = 'article'


class Pic(models.Model):
    img = models.ImageField(upload_to='img')

    class Meta:
        db_table = 'article_pic'
