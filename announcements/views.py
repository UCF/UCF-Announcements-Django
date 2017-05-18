from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from taggit.models import Tag

from announcements.decorators import user_is_authorized_editor
from announcements.models import *
from announcements.forms import *
from announcements.serializers import *

import util

# Create your views here.
class RemoteMenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(RemoteMenuMixin, self).get_context_data(**kwargs)

        header_menu_items = util.get_header_menu_items()
        footer_menu_items = util.get_footer_menu_items()

        context['header_menu_items'] = header_menu_items
        context['footer_menu_items'] = footer_menu_items

        return context

class HomeView(RemoteMenuMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        main_filter = self.request.GET.get('time', 'this-week')

        # Get the initial queryset
        items = self.get_initial_data(main_filter)

        audience = self.request.GET.get('audience', None)
        if audience is not None:
            items = items.filter(audience__name=audience)

        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            items = items.filter(keywords__name=keyword)

        context['announcements'] = items
        context['audiences'] = Audience.objects.all()
        return context

    def get_initial_data(self, time='this-week'):
        if time == 'this-week':
            return Announcement.objects.this_week()
        elif time == 'ongoing':
            return Announcement.objects.ongoing()
        elif time == 'upcoming':
            return Announcement.objects.upcoming()
        else:
            return Announcement.objects.this_week()

class AnnouncementDetail(RemoteMenuMixin, DetailView):
    model = Announcement
    template_name = 'announcements/announcement-detail.html'


@method_decorator(login_required, name='dispatch')
class AnnouncementListView(TemplateView):
    template_name = 'manager/announcements-list.html'

    def get_context_data(self, *args):
        context = super(AnnouncementListView, self).get_context_data(*args)
        announcements = Announcement.objects.owned_by(self.request.user)
        context['published'] = announcements.filter(status='Publish')
        context['pending'] = announcements.filter(status='Pending')
        return context

@method_decorator(login_required, name='dispatch')
class CreateAnnouncement(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'manager/announcement-create.html'
    success_url = reverse_lazy('announcements.manager')

    # Set posted_by and status automatically
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "Pending"
        return super(CreateAnnouncement, self).form_valid(form)

@method_decorator([login_required, user_is_authorized_editor], name='dispatch')
class EditAnnouncement(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'manager/announcement-edit.html'
    success_url = reverse_lazy('announcements.manager')

    # Make sure status is set to the current status if not updated
    def form_valid(self, form):
        if 'status' not in form.cleaned_data:
            form.instance.status = "Pending"

        return super(EditorAnnouncement, self).form_valid(form)

# API Views

class AnnouncementListAPIView(APIView):
    def get(self, request, format=None):
        announcements = Announcement.objects.this_week()
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)


class AnnouncementSyndicateView(CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_class = (IsAdminUser,)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class KeywordListAPIView(APIView):
    def get(self, request, format=None):
        s = request.query_params.get('s', None)
        keywords = None
        if s is not None:
            keywords = Tag.objects.filter(name__contains=s)
        else:
            keywords = Tag.objects.all()[:10]

        serializer = TagSerializer(keywords, many=True)
        return Response(serializer.data)
