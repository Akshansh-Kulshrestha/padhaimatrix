from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Specialization, Subject, Unit, Topic


# 🔥 INLINE (Specializations inside Course)
class SpecializationInline(admin.TabularInline):
    model = Specialization
    extra = 1


# 🔥 COURSE ADMIN
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SpecializationInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"


# 🔥 SPECIALIZATION ADMIN
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'image_preview')
    list_filter = ('course',)
    search_fields = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return "-"


# 🔥 SUBJECT ADMIN
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'get_course')
    list_filter = ('specialization',)
    search_fields = ('name',)

    def get_course(self, obj):
        return obj.specialization.course.name
    get_course.short_description = "Course"


# 🔥 UNIT ADMIN
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'get_specialization')
    list_filter = ('subject',)
    search_fields = ('name',)

    def get_specialization(self, obj):
        return obj.subject.specialization.name
    get_specialization.short_description = "Specialization"


# 🔥 TOPIC ADMIN
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'get_subject', 'get_course')
    list_filter = ('unit',)
    search_fields = ('name',)

    def get_subject(self, obj):
        return obj.unit.subject.name
    get_subject.short_description = "Subject"

    def get_course(self, obj):
        return obj.unit.subject.specialization.course.name
    get_course.short_description = "Course"