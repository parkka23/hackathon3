from django.db import models
from django.utils.text import slugify

from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    slug = models.SlugField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
