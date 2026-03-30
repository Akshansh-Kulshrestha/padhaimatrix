# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from users.User.models import User
from users.StudentProfile.models import StudentProfile
from users.TeacherProfile.models import TeacherProfile
from users.StaffProfile.models import StaffProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.get_or_create(user=instance)

        elif instance.role == 'teacher':
            TeacherProfile.objects.get_or_create(user=instance)

        elif instance.role in ['admin', 'staff']:
            StaffProfile.objects.get_or_create(user=instance)