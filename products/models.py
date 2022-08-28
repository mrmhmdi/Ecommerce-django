from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.files import File

from PIL import Image
from io import BytesIO
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True,)

    class Meta:
        ordering = ('-name',)

    # def get_absolute_url(self):
    #     return reverse("shop", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True)
    thumbnail = models.ImageField(upload_to='product_thumbnails/', blank=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            print(self.thumbnail.url)
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self._create_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'

    def _create_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def __str__(self) -> str:
        return self.name
