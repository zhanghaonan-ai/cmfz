from django.db import models


# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    broadcast = models.CharField(max_length=20,null=True)
    chapter_count = models.IntegerField(null=True,default=0)
    content = models.TextField(null=True)
    score = models.SmallIntegerField(default=5)
    publish_time = models.DateTimeField(auto_now_add=True)
    img_src = models.ImageField(upload_to='img')

    class Meta:
        db_table = 'album'


class Chapter(models.Model):
    title = models.CharField(max_length=20)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.FileField(upload_to='video')
    time_long = models.SmallIntegerField(null=True)
    album_id = models.IntegerField()

    class Meta:
        db_table = 'chapter'
