from django.db import models


# Create your models here.

class Carousel(models.Model):
    title = models.CharField(max_length=20)
    publish_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    img_url = models.ImageField(upload_to='carousel')

    class Meta:
        db_table = 'carousel'
