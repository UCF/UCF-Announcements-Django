from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from announcements.views import *

urlpatterns = [
    path(
        'manager/',
        AnnouncementListView.as_view(),
        name='announcements.manager'
    ),
    path(
        'manager/login/',
        LoginView.as_view(),
        kwargs={
            'template_name': 'manager/login.html'
        },
        name='django.contrib.auth.views.login'
    ),
    path(
        'manager/logout/',
        LogoutView.as_view(),
        name='django.contrib.auth.views.logout'
    ),
    path(
        'manager/post-an-announcement/',
        CreateAnnouncement.as_view(),
        name="announcements.manager.create"
    ),
    path(
        'manager/edit-announcement/<str:slug>/',
        EditAnnouncement.as_view(),
        name="announcements.manager.edit"
    ),
    path(
        'manager/delete-announcement/<str:slug>/',
        DeleteAnnouncement.as_view(),
        name="announcements.manager.delete"
    ),
    path(
        'manager/confirm-new-user/',
        confirm_user_view,
        name='announcements.manager.confirmuser'
    ),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    path(
        'api/announcements/',
        AnnouncementListAPIView.as_view(),
        name="announcements.api.list"
    ),
    path(
        'api/announcements/<int:pk>/',
        AnnouncementDetailAPIView.as_view(),
        name="announcements.api.detail"
    ),
    path(
        'api/keywords/',
        KeywordListAPIView.as_view(),
        name="announcements.api.keywords"
    ),
    path(
        'api/syndicate/',
        AnnouncementSyndicateView.as_view(),
        name="announcements.api.syndicate"
    ),
    path(
        '<str:slug>/',
        AnnouncementDetail.as_view(),
        name="announcements.detail"
    ),
    path(
        '',
        HomeView.as_view(),
        name="announcements.home"
    ),
]
