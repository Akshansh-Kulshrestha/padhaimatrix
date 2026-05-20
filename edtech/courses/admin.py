from django.contrib import admin
from .models import Specialization, CourseLevel, Course, Semester, Subject, Unit, Topic

# 1. Specialization Admin - Standard setup
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 2. Course Level Admin
@admin.register(CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

# 3. Course Admin - Handles Many-to-Many Specializations
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'is_published')
    list_filter = ('level', 'is_published')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # Use filter_horizontal for a better UI to pick shared Specializations
    filter_horizontal = ('specializations',)

# 4. Semester Admin
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('get_course_name', 'number')
    list_filter = ('course',)
    
    def get_course_name(self, obj):
        return obj.course.name
    get_course_name.short_description = 'Course'

# 5. Subject Admin - Grouped by Semester and Course
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_semester', 'get_course')
    list_filter = ('semester__course', 'semester')
    
    def get_semester(self, obj):
        return f"Sem {obj.semester.number}"
    get_semester.short_description = 'Semester'
    
    def get_course(self, obj):
        return obj.semester.course.name
    get_course.short_description = 'Course'

# 6. Unit Admin
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    list_filter = ('subject__semester__course', 'subject')

# 7. Topic Admin - The Content Editor
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'get_subject', 'get_course')
    list_filter = ('unit__subject__semester__course',)
    search_fields = ('name', 'content')

    def get_subject(self, obj):
        return obj.unit.subject.name
    get_subject.short_description = 'Subject'

    def get_course(self, obj):
        return obj.unit.subject.semester.course.name
    get_course.short_description = 'Course'