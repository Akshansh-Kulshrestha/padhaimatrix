from django.contrib import admin
from .models import CourseLevel, Specialization, Subject, Topic, UserProgress


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