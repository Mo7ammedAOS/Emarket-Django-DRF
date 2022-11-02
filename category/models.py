from enum import unique
from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.text import slugify


# Create your models here.

def uploaded_photos(instance , filename):
    imagename , extension = filename.split('.')
    return 'photos/categories/%s.%s'%(instance.id ,extension)

class Category(models.Model):
    category_name  = models.CharField(max_length = 50 , unique = True)
    description    = models.TextField(max_length = 100 , blank = True)
    category_image = models.ImageField(upload_to = uploaded_photos)
    slug           = models.SlugField(max_length = 50 , unique = True , blank = True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('store:productByCatg',args=[self.slug])

    def save(self,*args,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.category_name