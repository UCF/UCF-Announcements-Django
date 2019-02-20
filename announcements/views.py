from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, View, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.sitemaps import Sitemap
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from taggit.models import Tag

from announcements.decorators import user_is_authorized_editor
from announcements.models import *
from announcements.forms import *
from announcements.serializers import *
from announcements.filters import *

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

class StaticSiteMap(Sitemap):
    priority = 0.5;
    changefreq = 'daily'

    def items(self):
        return ['announcements.home']

    def lastmod(self, obj):
        return datetime.date.today()

    def location(self, item):
        return reverse(item)

class AnnouncementSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Announcement.objects.active()

    def lastmod(self, obj):
        return obj.start_date

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('announcements.home')

class HomeView(RemoteMenuMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        main_filter = self.request.GET.get('time', 'this-week')

        # Get the initial queryset
        items = self.get_initial_data(main_filter)
        ongoing = self.get_initial_data('ongoing')

        audience = self.request.GET.get('audience', None)
        if audience is not None:
            items = items.filter(audience__name=audience)

        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            items = items.filter(keywords__name=keyword)

        if main_filter != 'ongoing':
            items = list(set(items) - set(ongoing))

        context['announcements'] = items
        context['ongoing'] = ongoing
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
        announcements = Announcement.objects.owned_by(self.request.user, True)
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
        if not self.request.user.is_superuser:
            form.instance.status = "Pending"
        return super(CreateAnnouncement, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateAnnouncement, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

@method_decorator([login_required, user_is_authorized_editor], name='dispatch')
class EditAnnouncement(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'manager/announcement-edit.html'
    success_url = reverse_lazy('announcements.manager')

    def get_form_kwargs(self):
        kwargs = super(EditAnnouncement, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class DeleteAnnouncement(DeleteView):
    model = Announcement
    template_name = 'manager/announcement-delete.html'
    success_url = reverse_lazy('announcements.manager')

    def get(self, *args, **kwargs):
        obj = self.get_object()
        if obj.is_owner(self.request.user):
            return super(DeleteAnnouncement, self).get(*args, **kwargs)
        else:
            return redirect( reverse_lazy( 'announcements.manager' ), True )

# API Views

class AnnouncementListAPIView(ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    filter_class = AnnouncementFilter

    def get_queryset(self):
        time = self.request.query_params.get('time', None)
        exclude_ongoing = self.request.query_params.get('exclude_ongoing', False)
        audience = self.request.query_params.get('audience', None)

        queryset = Announcement.objects.all()

        if time is not None:
            if time == 'this-week':
                queryset = Announcement.objects.this_week()
            if time == 'ongoing':
                queryset = Announcement.objects.ongoing()
            elif time == 'upcoming':
                queryset = Announcement.objects.upcoming()
            else:
                queryset = Announcement.objects.this_week()
        else:
            queryset = Announcement.objects.this_week()

        if audience is not None:
            queryset = queryset.filter(audience__name=audience)

        if exclude_ongoing and Announcement.objects.ongoing().count() > 0:
            queryset = queryset.exclude(pk__in=Announcement.objects.ongoing().values_list('pk', flat=True))

        return queryset

class AnnouncementDetailAPIView(RetrieveAPIView):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

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

def confirm_user_view(request):
    if request.method == 'POST':
        request.user.profile.first_time = False
        request.user.profile.save()
        return HttpResponse('OK')
