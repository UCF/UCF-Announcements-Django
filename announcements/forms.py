from django import forms
from announcements.models import *

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'audience', 'start_date', 'end_date', 'url', 'contact_name', 'contact_phone', 'contact_email', 'keywords', 'posted_by', 'status']
        widgets = {
            'audience': forms.CheckboxSelectMultiple,
            'author': forms.HiddenInput,
            'status': forms.Select
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        
    def form_valid(self, form):
        print self.user
        self.object = form.save(commit=False)
        self.object.author = self.user
        self.object.status = 'Pending'
        self.object.save()