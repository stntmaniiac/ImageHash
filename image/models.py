from django.db import models
from django.urls import reverse


class Images(models.Model):
    title=models.CharField(max_length=120)
    content=models.TextField()
    imagesrc=models.FileField()
    hashvalue=models.CharField(max_length=32,null=True,blank=True)

    def get_absolute_url(self):
        return reverse('image:details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def __int__(self, title, content, imagesrc, hashvalue):
        self.title=title
        self.content=content
        self.imagesrc=imagesrc
        self.hashvalue=hashvalue
