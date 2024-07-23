from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)

    # To change the string representation, we have to define the __str__() function of the Member Model in models.py
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

# Create a model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft',
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published_at')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blog_posts', default=1)
    body = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager() # The default manager
    published = PublishedManager() # A custom manager for published posts

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['published_at']),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blogsite:post_detail', 
                       args=[self.published_at.year,
                             self.published_at.month,
                             self.published_at.day,
                             self.slug,]
    )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"