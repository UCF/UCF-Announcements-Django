from django.conf.urls import include, url

from django.contrib.auth.views import login, logout
from announcements.views import *

urlpatterns = [
    url(r'^manager/$', AnnouncementListView.as_view(), name='announcements.manager'),
    url(r'^manager/login/$', login, kwargs={'template_name': 'manager/login.html'}, name='django.contrib.auth.views.login'),
    url(r'^manager/logout/$', LogoutView.as_view(), name='django.contrib.auth.views.logout'),
    url(r'^manager/post-an-announcement[/]?$', CreateAnnouncement.as_view(), name="announcements.manager.create"),
    url(r'^manager/edit-announcement/(?P<slug>[-\w]+)/', EditAnnouncement.as_view(), name="announcements.manager.edit"),
    url(r'^manager/delete-announcement/(?P<slug>[-\w]+)/', DeleteAnnouncement.as_view(), name="announcements.manager.delete"),
    url(r'^manager/confirm-new-user[/]?$', confirm_user_view, name='announcements.manager.confirmuser'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/announcements[/]?$', AnnouncementListAPIView.as_view(), name="announcements.api.list"),
    url(r'^api/keywords[/]?$', KeywordListAPIView.as_view(), name="announcements.api.keywords"),
    url(r'^api/syndicate[/]?$', AnnouncementSyndicateView.as_view(), name="announcements.api.syndicate"),
    url(r'^(?P<slug>[-\w]+)/', AnnouncementDetail.as_view(), name="announcements.detail"),
    url(r'^$', HomeView.as_view(), name="announcements.home"),
]
