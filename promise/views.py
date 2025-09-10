from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Profile, Publication, Project, Skill, Education, Feedback, Video
from django import forms
import logging

logger = logging.getLogger(__name__)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'whatsapp', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'required': 'required', 'aria-describedby': 'name-error'}),
            'email': forms.EmailInput(attrs={'required': 'required', 'aria-describedby': 'email-error'}),
            'whatsapp': forms.TextInput(attrs={'pattern': r'^\+\d{1,13}$', 'aria-describedby': 'whatsapp-error'}),
            'message': forms.Textarea(attrs={'required': 'required', 'aria-describedby': 'message-error'})
        }

def home(request):
    profile = Profile.objects.first()
    publications = Publication.objects.all()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    educations = Education.objects.all()
    videos = Video.objects.all()

    # Log image paths and video URLs for debugging
    logger.info(f"Profile photo: {profile.photo.url if profile and profile.photo else 'None'}")
    for project in projects:
        logger.info(f"Project {project.title} image: {project.image.url if project.image else 'None'}")
    for pub in publications:
        logger.info(f"Publication {pub.title} image: {pub.image.url if pub.image else 'None'}")
    for video in videos:
        logger.info(f"Video {video.title} URL: {video.url}")

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({'success': True}, status=200)
            messages.success(request, "Thank you for your feedback!")
            return redirect('home')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedbackForm()

    if not profile:
        profile = Profile(
            name="Default User",
            bio="No profile information available.",
            twitter="https://twitter.com",
            facebook="https://facebook.com/nasim.promise03",
            linkedin="https://linkedin.com",
            instagram="https://instagram.com"
        )

    return render(request, "home.html", {
        "user": profile,
        "publications": publications,
        "projects": projects,
        "skills": skills,
        "educations": educations,
        "videos": videos,
        "feedback_form": form
    })
