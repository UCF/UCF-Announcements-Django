"""
Specifies the announcement models
"""
from __future__ import unicode_literals
import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

from bleach import linkify

from rest_framework.authtoken.models import Token

import settings

# Create your models here.

class Audience(models.Model):
    """
    The Audience Model for storing various audience roles

    Attributes:
        name (str): The name of the audience
    """
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class AnnouncementManager(models.Manager):
    """
    Provides a manager for retrieving announcements
    """
    def this_week(self):
        """
        Returns announcements from the most recent monday until
        the following Sunday
        """
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        next_sunday = last_monday + datetime.timedelta(days=6)
        return self.filter(start_date__lte=next_sunday, end_date__gte=last_monday, status='Publish')

    def ongoing(self):
        """
        Returns announcements that fall outside of this week
        """
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        next_sunday = last_monday + datetime.timedelta(days=6)

        return self.filter(start_date__lt=last_monday, end_date__gt=next_sunday, status='Publish')

    def upcoming(self):
        """
        Returns announcements that begin after next Sunday
        """
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        next_sunday = last_monday + datetime.timedelta(days=6)
        return self.filter(start_date__gte=next_sunday, status='Publish')

    def owned_by(self, user=None, future=True):
        """
        Returns events owned by the user

        Args:
            user (User): A User object
        """
        today = datetime.date.today()

        if user.is_staff:
            retval = self.all()
        else:
            retval = self.filter(author=user)

        if future:
            retval = retval.filter(end_date__gte=today)

        return retval.order_by('-start_date') #order by descensing `-`

class Announcement(models.Model):
    """
    An Announcement Model

    Attributes:
        title (str): The announcement's title
        slug (str): The unique slug of the announcement
        description (str): The content of the announcement
        audience (Audience[]): One or many audiences
        keywords (Tag[]): One or many keywords (tags)
        start_date (datetime): The start date of the announcement
        end_date (datetime): The end date of the announcement
        url (str): The url to send users to for more information
        contact_name (str): The contact person for the announcement
        contact_phone (str): The phone number for the contact person
        contact_email (str): The email address of the conteact person
        poste_by (str): The person or organization posting the annnouncement
        status (str): The status of the announcement
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=128, null=False, blank=True, unique=True)
    description = models.TextField(null=False, blank=False)
    audience = models.ManyToManyField(Audience, related_name='announcements')
    keywords = TaggableManager()
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    url = models.URLField(null=True, blank=True)
    contact_name = models.CharField(max_length=100, null=False, blank=False)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    contact_email = models.CharField(max_length=100, null=False, blank=False)
    posted_by = models.CharField(max_length=255, null=False, blank=False)
    author = models.ForeignKey(User, related_name='announcements', blank=True, null=True)

    statuses = (
        ('Pending', 'Pending'),
        ('Publish', 'Publish')
    )

    status = models.CharField(max_length=7, blank=True, null=False, choices=statuses)
    objects = AnnouncementManager()

    def save(self, *args, **kwargs):
        """
        Handles additional save functions
        """
        if not self.id or self.slug is None:
            self.slug = self.unique_slug(self.title)

        if self.description:
            self.description  = linkify(self.description)

        super(Announcement, self).save(*args, **kwargs)

    def unique_slug(self, title):
        retval = slugify(title)

        exists = Announcement.objects.filter(slug=retval).exists()
        i = 0

        while exists:
            i += 1
            retval = retval + '-' + str(i)
            exists = Announcement.objects.filter(slug=retval).exists()

        return retval

    def is_owner(self, user=None):
        """
        Determines if the provided user is the owner

        Attributes:
            user (User): The user to check
        """
        if self.author == user or user.is_staff:
            return True
        else:
            return False

    def permalink(self):
        return reverse_lazy('announcements.detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode(self):
        return self.title

class Profile(models.Model):
    """
    A User Profile
    """
    user = models.OneToOneField(User, related_name='profile')
    guid = models.CharField(max_length=100, null=True, unique=True)
    first_time = models.BooleanField(default=True)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created=False, **kwargs):
    """
    Create a token on user create
    """
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)
