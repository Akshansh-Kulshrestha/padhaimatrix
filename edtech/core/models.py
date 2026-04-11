from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
import uuid


User = settings.AUTH_USER_MODEL

# Base Class to save repeating the Slug logic for every model
class BaseEduModel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

class CourseLevel(BaseEduModel):
    class Meta:
        verbose_name_plural = "Course Levels"

class Specialization(BaseEduModel):
    courselevel = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name="specializations")

class Subject(BaseEduModel):
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name="subjects")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="subject_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
class Topic(BaseEduModel):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")
    
    content = RichTextUploadingField(blank=True, null=True)
    
# Metadata for the individual lesson
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Topics"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic') # Ensures a topic isn't counted twice