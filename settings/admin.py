from django.contrib import admin
from .models import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'notifications_enabled', 'language', 'updated_at')
    list_filter = ('theme', 'notifications_enabled', 'language', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Preferências de Interface', {
            'fields': ('theme', 'language')
        }),
        ('Notificações', {
            'fields': ('notifications_enabled',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
