from django.core.exceptions import PermissionDenied
from announcements.models import Announcement

def user_is_authorized_editor(function):
    """
    Decorator that determines if the user owns an annnouncement
    """
    def wrap(request, *args, **kwargs):
        """
        Wrapper for the decorator
        """
        announcement = Announcement.objects.get(slug=kwargs['slug'])
        if announcement.author == request.user or request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
