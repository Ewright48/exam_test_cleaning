from django.contrib import admin
from .models import User, Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'application_date', 'application_time', 'status', 'service', 'payment']
    list_filter = ['status', 'application_date']
    list_editable = ['status']
    search_fields = ['user__username']
    list_per_page = 5

admin.site.register(User)