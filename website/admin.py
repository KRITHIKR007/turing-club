from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _
from .models import Event, Project, Article, GalleryImage, Achievement, TeamMember
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils import timezone

# Custom Admin Site
class TuringClubAdminSite(admin.AdminSite):
    site_header = 'Turing Club Portfolio Administration'
    site_title = 'Turing Club Admin'
    index_title = 'Turing Club Dashboard'
    
    def get_app_list(self, request):
        """
        Return sorted app list for dashboard
        """
        app_list = super().get_app_list(request)
        # Sort the apps alphabetically
        app_list.sort(key=lambda x: x['name'].lower())
        # Sort the models alphabetically within each app
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return app_list
    
    def index(self, request, extra_context=None):
        """
        Customize the admin index page with summary statistics
        """
        from website.models import Event, Project, Article, TeamMember, GalleryImage
        
        # Get model statistics
        stats = {
            'events': {
                'total': Event.objects.count(),
                'upcoming': Event.objects.filter(date__gte=timezone.now().date()).count(),
            },
            'projects': {
                'total': Project.objects.count(),
            },
            'articles': {
                'total': Article.objects.count(),
                'published': Article.objects.filter(published=True).count(),
            },
            'team_members': {
                'total': TeamMember.objects.count(),
                'core': TeamMember.objects.filter(is_core_member=True).count(),
            },
            'gallery': {
                'total': GalleryImage.objects.count(),
            }
        }
        
        # Build dashboard HTML
        dashboard_html = """
        <div style="padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 5px;">
            <h2 style="margin-top: 0;">Turing Club Dashboard</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 15px;">
                <div style="flex: 1; min-width: 200px; padding: 15px; background-color: #007bff; color: white; border-radius: 5px;">
                    <h3>Events</h3>
                    <p>Total: {events[total]}</p>
                    <p>Upcoming: {events[upcoming]}</p>
                </div>
                <div style="flex: 1; min-width: 200px; padding: 15px; background-color: #28a745; color: white; border-radius: 5px;">
                    <h3>Projects</h3>
                    <p>Total: {projects[total]}</p>
                </div>
                <div style="flex: 1; min-width: 200px; padding: 15px; background-color: #ffc107; color: white; border-radius: 5px;">
                    <h3>Articles</h3>
                    <p>Total: {articles[total]}</p>
                    <p>Published: {articles[published]}</p>
                </div>
                <div style="flex: 1; min-width: 200px; padding: 15px; background-color: #17a2b8; color: white; border-radius: 5px;">
                    <h3>Team</h3>
                    <p>Total Members: {team_members[total]}</p>
                    <p>Core Members: {team_members[core]}</p>
                </div>
                <div style="flex: 1; min-width: 200px; padding: 15px; background-color: #6f42c1; color: white; border-radius: 5px;">
                    <h3>Gallery</h3>
                    <p>Total Images: {gallery[total]}</p>
                </div>
            </div>
        </div>
        """.format(**{
            'events': stats['events'],
            'projects': stats['projects'],
            'articles': stats['articles'],
            'team_members': stats['team_members'], 
            'gallery': stats['gallery'],
        })
        
        context = extra_context or {}
        context.update({
            'dashboard_html': mark_safe(dashboard_html),
        })
        return super().index(request, context)

admin_site = TuringClubAdminSite(name='turingadmin')

# Model admin classes
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_featured', 'display_image')
    list_filter = ('is_featured', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    list_per_page = 15
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'date', 'location', 'is_featured')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'project_url', 'is_featured', 'display_image')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_per_page = 15
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'technologies', 'project_url', 'github_url', 'is_featured')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_featured', 'display_image')
    list_filter = ('is_featured', 'author', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 15
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'slug', 'author', 'content', 'is_featured')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'created_at', 'display_image')
    list_filter = ('event', 'created_at')
    search_fields = ('title',)
    list_per_page = 15
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'event')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'display_image')
    list_filter = ('date',)
    search_fields = ('title', 'description')
    list_per_page = 15
    fieldsets = (
        ('Achievement Information', {
            'fields': ('title', 'description', 'date')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_core_member', 'order', 'display_image')
    list_filter = ('is_core_member', 'position', 'joining_date')
    search_fields = ('name', 'position', 'bio')
    list_per_page = 15
    actions = ['make_core_member', 'remove_core_member', 'reset_display_order']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'position', 'bio', 'joining_date')
        }),
        ('Display Options', {
            'fields': ('is_core_member', 'order')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Social Links', {
            'fields': ('email', 'linkedin_url', 'github_url'),
            'classes': ('collapse',),
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'
    
    def make_core_member(self, request, queryset):
        queryset.update(is_core_member=True)
        self.message_user(request, f"{queryset.count()} team member(s) marked as core members.")
    make_core_member.short_description = "Mark selected members as core members"
    
    def remove_core_member(self, request, queryset):
        queryset.update(is_core_member=False)
        self.message_user(request, f"{queryset.count()} team member(s) removed from core members.")
    remove_core_member.short_description = "Remove selected members from core team"
    
    def reset_display_order(self, request, queryset):
        for i, member in enumerate(queryset.order_by('name')):
            member.order = i + 1
            member.save()
        self.message_user(request, f"Display order reset for {queryset.count()} team member(s).")
    reset_display_order.short_description = "Reset display order for selected members"

# Register models with our custom admin site
admin_site.register(Event, EventAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(Article, ArticleAdmin)
admin_site.register(GalleryImage, GalleryImageAdmin)
admin_site.register(Achievement, AchievementAdmin)
admin_site.register(TeamMember, TeamMemberAdmin)
admin_site.register(LogEntry)

# Keep the default admin site registration for backwards compatibility
# This allows us to still use the default admin site if needed
@admin.register(Event)
class DefaultEventAdmin(EventAdmin):
    pass

@admin.register(Project)
class DefaultProjectAdmin(ProjectAdmin):
    pass

@admin.register(Article)
class DefaultArticleAdmin(ArticleAdmin):
    pass

@admin.register(GalleryImage)
class DefaultGalleryImageAdmin(GalleryImageAdmin):
    pass

@admin.register(Achievement)
class DefaultAchievementAdmin(AchievementAdmin):
    pass

@admin.register(TeamMember)
class DefaultTeamMemberAdmin(TeamMemberAdmin):
    pass
