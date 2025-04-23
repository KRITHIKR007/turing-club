from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Tags as a comma-separated string, e.g. "Web Dev,AI/ML,IoT"
    tags = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return self.title
        
    def get_tags_list(self):
        """Return tags as a list of strings"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
        
    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies = models.CharField(max_length=200)  # Comma-separated list of technologies
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
    def get_technologies_list(self):
        """Return technologies as a list of strings"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []
        
    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='gallery_images')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    is_core_member = models.BooleanField(default=False)
    joining_date = models.DateField(default=timezone.now)
    order = models.IntegerField(default=0, help_text="Display order on team page")
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name
