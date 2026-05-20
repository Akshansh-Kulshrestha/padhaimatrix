from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# 1. SHARED SPECIALIZATIONS
# Now 'CSE' or 'Robotics' exists once and can be linked to B.Tech, Diploma, or PhD.
class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

# 2. COURSE LEVELS (From your PDF: Beginner, Graduate, etc.)
class CourseLevel(models.Model):
    name = models.CharField(max_length=100) # Beginner, Graduate, etc. 
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

# 3. COURSE (e.g., B.Tech, MSc, Class 1-5)
class Course(models.Model):
    level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100) # 
    # This ManyToMany allows specializations to be "the same for all courses"
    specializations = models.ManyToManyField(Specialization, related_name="courses")
    image = models.ImageField(upload_to='course_image/')
    description = models.TextField(max_length=1000)
    slug = models.SlugField(unique=True, blank=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# 4. SEMESTER (Linked to Course)
class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="semesters")
    number = models.IntegerField() # 

    def __str__(self):
        return f"{self.course.name} - Sem {self.number}"

# 5. SUBJECT -> UNIT -> TOPIC (Content Chain)
class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100) # 
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="units")
    name = models.CharField(max_length=100) # 

class Topic(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=100) # 
    # Professional feature: Rich Text for formatted lessons
    content = RichTextUploadingField() 

    def __str__(self):
        return self.name
    