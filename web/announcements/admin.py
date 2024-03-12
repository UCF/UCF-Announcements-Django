from django.contrib import admin
from announcements.models import *
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    pass

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass

TokenAdmin.raw_id_fields = ('user',)
