from django.db import models

# Create your models here.
class TeacherProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    expertise = models.CharField(max_length=255)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username