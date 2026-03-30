from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

User = settings.AUTH_USER_MODEL

class CourseLevel(models.Model):
    name = models.CharField(max_length=100)  # B.Tech, Class 12

    def __str__(self):
        return self.name
    
class Specialization(models.Model):
    name = models.CharField(max_length=100)  # CSE, IT
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)  # DSA, DBMS
    image = models.ImageField(upload_to='subjects/')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)  # Linked List, Trees
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)



    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 🔥 FILTER SYSTEM
    course_level = models.ForeignKey(CourseLevel, on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    tags = models.CharField(max_length=255, blank=True)

    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ArticleCorrection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    suggested_title = models.CharField(max_length=255, blank=True)
    suggested_content = models.TextField()

    comment = models.TextField(blank=True)  # why correction

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_corrections")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correction for {self.article.title}"
    
class ArticleSuggestion(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField()

    course_level = models.ForeignKey("CourseLevel", on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey("Specialization", on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey("Topic", on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_suggestions")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title