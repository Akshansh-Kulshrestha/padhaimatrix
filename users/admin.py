from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.User.models import *
from users.StudentProfile.models import StudentProfile
from users.TeacherProfile.models import TeacherProfile
from users.StaffProfile.models import StaffProfile
from users.Organization.models import Organization
from users.UserOrganization.models import UserOrganization

from .models import *

admin.site.register(User)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Qualification)

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ('username', 'email',  'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_active')

#     fieldsets = BaseUserAdmin.fieldsets + (
#         ('Additional Info', {
#             'fields': ('role', 'phone','is_phone_verified', 'is_verified', 'dob', 'occupation', 'institute', 'address',)
#         }),
#     )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education_level', 'institution')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'experience_years')


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(UserOrganization)
class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role')