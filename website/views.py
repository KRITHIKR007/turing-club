from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Event, Project, Article, GalleryImage, Achievement

# Homepage view
def index(request):
    # Get featured content for homepage
    featured_events = Event.objects.filter(is_featured=True).order_by('-date')[:3]
    featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:3]
    featured_articles = Article.objects.filter(is_featured=True).order_by('-created_at')[:3]
    gallery_images = GalleryImage.objects.all().order_by('-created_at')[:8]
    achievements = Achievement.objects.all().order_by('-date')[:4]
    
    context = {
        'featured_events': featured_events,
        'featured_projects': featured_projects,
        'featured_articles': featured_articles,
        'gallery_images': gallery_images,
        'achievements': achievements
    }
    return render(request, 'index.html', context)

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            # Log the user in after signup
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Profile view - requires login
@login_required
def profile(request):
    return render(request, 'registration/profile.html')

# Project views
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'website/project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return redirect(project.project_url)  # Redirect to external URL when view project button is clicked

# Article views
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'website/article_list.html', {'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'website/article_detail.html', {'article': article})

# Event views
def event_list(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    return render(request, 'website/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    related_images = event.gallery_images.all()
    return render(request, 'website/event_detail.html', {
        'event': event,
        'related_images': related_images
    })

# Gallery view
def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    events = Event.objects.all().order_by('-date')
    return render(request, 'website/gallery.html', {
        'images': images,
        'events': events
    })
