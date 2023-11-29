from django.db import models


class News(models.Model):
    photo = models.URLField()
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    date = models.CharField(max_length=12)

    class Meta:
        db_table = 'LatestNews'