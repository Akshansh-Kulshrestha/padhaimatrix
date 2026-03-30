from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    education_level = models.CharField(max_length=100)
    institution = models.CharField(max_length=255, blank=True, null=True)

    # enrolled_courses = models.ManyToManyField('courses.Course', blank=True)

    def __str__(self):
        return self.user.username