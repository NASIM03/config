from django.db import models
from django.core.validators import EmailValidator, RegexValidator, URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class Profile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload a PDF resume (e.g., resume.pdf)"
    )
    twitter = models.URLField(blank=True, null=True, validators=[URLValidator()])
    facebook = models.URLField(blank=True, null=True, validators=[URLValidator()])
    linkedin = models.URLField(blank=True, null=True, validators=[URLValidator()])
    instagram = models.URLField(blank=True, null=True, validators=[URLValidator()])

    def clean(self):
        social_fields = {
            'twitter': 'twitter.com',
            'facebook': 'facebook.com',
            'linkedin': 'linkedin.com',
            'instagram': 'instagram.com'
        }
        for field, domain in social_fields.items():
            url = getattr(self, field)
            if url:
                if not (url.startswith('http://') or url.startswith('https://')):
                    raise ValidationError({field: f"{field.capitalize()} URL must start with http:// or https://"})
                if domain not in url.lower():
                    raise ValidationError({field: f"{field.capitalize()} URL must point to {domain}"})

    def __str__(self):
        return self.name

class Publication(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    journal = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    link = models.URLField(blank=True, null=True, validators=[URLValidator()])
    image = models.ImageField(upload_to='publications/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True,
                            help_text="Comma-separated list of tags (e.g., HCI, ICT)")

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()] if self.tags else []

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    link = models.URLField(blank=True, null=True, validators=[URLValidator()])
    language = models.CharField(max_length=200, blank=True, null=True,
                               help_text="Comma-separated list of languages (e.g., Python, JavaScript)")

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Education(models.Model):
    degree = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    institute = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.degree} at {self.institute}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    whatsapp = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            r'^\+\d{1,13}$',
            message="Enter a valid WhatsApp number with country code (e.g., +12025550123)"
        )]
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"

class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_youtube_id(self):
        match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)", self.url)
        return match.group(1) if match else None

    def __str__(self):
        return self.title
