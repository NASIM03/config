from django.contrib import admin
from .models import Profile, Publication, Project, Skill, Education, Feedback, Video

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'twitter', 'facebook', 'linkedin', 'instagram']
    fieldsets = (
        (None, {
            'fields': ('name', 'bio', 'photo', 'resume')
        }),
        ('Social Media', {
            'fields': ('twitter', 'facebook', 'linkedin', 'instagram'),
            'description': 'Enter full URLs (e.g., https://twitter.com/username) for social media profiles.'
        }),
    )

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'journal')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'language')
    search_fields = ('title',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institute', 'start_year', 'end_year')
    list_filter = ('institute',)
    search_fields = ('degree', 'institute')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'url')
    readonly_fields = ('created_at',)