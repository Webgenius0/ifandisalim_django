from django.db import models

from ckeditor.fields import RichTextField

class StaticPages(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    # save slug from title
    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)
        


class ContactUs(models.Model):
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = RichTextField()
    order = models.PositiveIntegerField(default=0)
    # slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.question
    class Meta:
        ordering = ['order']
