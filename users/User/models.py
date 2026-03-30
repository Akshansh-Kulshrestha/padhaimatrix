from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):

    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('user', 'General User'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('rather_not_say', 'Rather Not Say'),
    )

    # 🔐 Core
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    # 👤 Profile
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)

    # 📱 Contact
    phone = models.CharField(max_length=15, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    # 🏢 Professional
    occupation = models.CharField(max_length=100, blank=True, null=True)
    institute = models.CharField(max_length=150, blank=True, null=True)

    # 🌍 Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    # 🔗 Social
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    # 🔒 System
    is_verified = models.BooleanField(default=False)
    is_erp_user = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# 🔥 MULTIPLE EXPERIENCE
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')

    company = models.CharField(max_length=150)
    role = models.CharField(max_length=100)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company} - {self.role}"


# 🎓 MULTIPLE EDUCATION
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')

    degree = models.CharField(max_length=150)
    institute = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)

    start_year = models.CharField(max_length=10, blank=True, null=True)
    end_year = models.CharField(max_length=10, blank=True, null=True)

    grade = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.degree} - {self.institute}"


# 📜 MULTIPLE QUALIFICATIONS / CERTIFICATIONS
class Qualification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qualifications')

    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, blank=True, null=True)

    issue_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title