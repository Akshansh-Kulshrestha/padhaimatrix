from django.contrib import admin
from .models import *

admin.site.register(Article)
admin.site.register(Topic)
admin.site.register(Specialization)
admin.site.register(Subject)
admin.site.register(CourseLevel)




@admin.register(ArticleCorrection)
class ArticleCorrectionAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(ArticleSuggestion)
class ArticleSuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status',)
    