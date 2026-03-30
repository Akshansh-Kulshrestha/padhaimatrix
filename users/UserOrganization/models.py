from django.db import models

# Create your models here.
class UserOrganization(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

    role = models.CharField(max_length=50)  # admin, teacher, etc.