from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True,)

    class Meta:
        ordering = ('-name',)

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"slug": self.slug})

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

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
