from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('profile/', views.profile, name='profile'),  # User profile page
    
    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    
    # Article URLs
    path('blog/', views.article_list, name='article_list'),
    path('blog/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    
    # Gallery URL
    path('gallery/', views.gallery, name='gallery'),
]