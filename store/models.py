from email.policy import default
from random import choices
from secrets import choice
from unicodedata import category
from django.db import models
from accounts.models import Account, UserProfile
from category.models import Category
from django.utils.text import slugify
from django.db.models import Avg , Count

# Create your models here.

def uploaded_photos(instance , filename):
    imagename , extension = filename.split('.')
    return 'photos/products/%s.%s'%(F'PRODUCT{instance.id}{instance.updated} ',extension)

class Product(models.Model):
    product_name = models.CharField(max_length = 200, unique = True)
    slug = models.SlugField(max_length = 200, unique = True, blank = True)
    description = models.TextField(max_length = 500, blank = True)
    price = models.IntegerField()
    images = models.ImageField(upload_to = uploaded_photos)
    stock = models.IntegerField()
    is_available = models.BooleanField(default = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
  

    

    def save(self,*args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)


    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRate.objects.filter(product = self, status = True).aggregate(av = Avg('rating'))
        avg = 0
        if reviews['av'] is not None:
            avg = float(reviews['av'])
            return avg

    def countRVid(self):
        reviews = ReviewRate.objects.filter(product = self, status = True).aggregate(count=Count('id'))
        count= None
        if reviews['count'] is not None:
            count = int(reviews['count'])
            return count

class VariationManger(models.Manager):

    def colors(self):
        return super(VariationManger,self).filter(variation_category= 'color',is_active = True)

    def sizes(self):
        return super(VariationManger,self).filter(variation_category= 'size',is_active = True)



variation_category_choice=(
    ('color','color'),
    ('size','size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    variation_category = models.CharField(max_length = 200 , choices = variation_category_choice)
    variation_value = models.CharField(max_length = 100)
    is_active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)

    objects = VariationManger()

    def __str__(self):
        return self.variation_value


class ReviewRate(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank = True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    review = models.TextField(max_length=500, blank = True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank = True)
    status = models.BooleanField(default = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.subject


def uploaded_photos(instance , filename):
    imagename , extension = filename.split('.')
    return 'photos/products_gallery/%s.%s'%(f'Pdt_Gellery_{instance.product.updated}' ,extension)

class Product_Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    image = models.ImageField(blank=True, upload_to= uploaded_photos, max_length=225) 

    class Meta:
        verbose_name = "Product_Gallery"
        verbose_name_plural = "Product Gallery"
    def __str__(self):
        return self.product.product_name