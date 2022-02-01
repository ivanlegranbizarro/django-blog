from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from autoslug import AutoSlugField
from tinymce.models import HTMLField


# Create your models here.


class Category(TimeStampedModel):
    """
    Category model
    """
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    """
    Model for blog posts
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 default='uncategorized')
    liked = models.ManyToManyField(User,
                                   related_name='liked_posts',
                                   default=None,
                                   blank=True)

    def total_likes(self):
        return self.liked.all().count()

    def __str__(self):
        return self.title


class Profile(TimeStampedModel):
    """
    Model for user profile
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profile/',
                              blank=True,
                              null=True)
    bio = HTMLField(blank=True, null=True)
    fb_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    insta_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)

    slug = AutoSlugField(populate_from='user', unique=True)

    def __str__(self):
        return f'Profile for {self.user.username}'


class Comment(TimeStampedModel):
    """
    Model for comments
    """
    name = models.CharField(max_length=100, blank=True, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = HTMLField(blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.name}'
