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
        help_texts = {
            'title': 'Enter a descriptive title',
            'description': 'The primary content of your announcement',
            'audience': 'Used for identifying the intended audience of this announcement',
            'start_date': 'When the announcement should begin appearing in feeds and emails',
            'end_date': 'When the announcement should stop appearing in feeds and emails',
            'url': 'A url where additional information realted to your announcement can be found',
            'contact_name': 'The name of the person or organization who can be contacted regarding this announcement',
            'contact_phone': 'The phone number of the contact person or organization',
            'contact_email': 'The email address of the contact person or organization',
            'keywords': 'Enter each keyword followed by a comma (or by pressing tab)',
            'posted_by': 'The name of the person or organization posting this announcement'
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(AnnouncementForm, self).__init__(*args, **kwargs)

        if self.user and not self.user.is_superuser:
            self.fields['status'].disabled = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.user
        self.object.save()
