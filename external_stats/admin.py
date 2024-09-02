from django.contrib import admin

from external_stats.api.models import ExternalInstallDay

admin.site.site_header = "External Apps Stats administration"


@admin.register(ExternalInstallDay)
class ExternalInstallDayAdmin(admin.ModelAdmin):
    """Admin class for the ExternalInstallDay model."""

    list_display = ('date', 'installations', 'wallpaper_count', 'applications')
    list_filter = ('date', 'installations', 'wallpaper_count')
    search_fields = ('date', 'installations', 'wallpaper_count', 'applications')
    ordering = ('-date',)
