import django_filters
from django_filters import rest_framework as filters

from announcements.models import *

class AnnouncementFilter(django_filters.FilterSet):
    search = filters.CharFilter(name='title', lookup_expr='icontains')

    class Meta:
        model = Announcement
        fields = (
            'search',
            'title',
            'start_date',
            'end_date',
            'posted_by',
            'status'
        )
