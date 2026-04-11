from django.contrib import admin
from .models import CourseLevel, Specialization, Subject, Topic, UserProgress, University, Notes, Software


@admin.register(CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'uuid')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'courselevel', 'code')
    list_filter = ('courselevel',)
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'code')
    list_filter = ('specialization__courselevel', 'specialization')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'code')
    list_filter = ('subject__specialization__courselevel', 'subject')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('user__username', 'topic__name')

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_published')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('name', 'uni_name', 'branch', 'semester', 'is_published')
    list_filter = ('uni_name', 'branch', 'semester')
    search_fields = ('name', 'uni_name__name', 'branch')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_published')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}