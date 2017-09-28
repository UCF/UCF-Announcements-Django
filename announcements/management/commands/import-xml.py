from django.core.management.base import BaseCommand, CommandError
from announcements.models import *

from argparse import FileType
from bs4 import BeautifulSoup as BS
from datetime import datetime
from markdown import markdown
from bleach import linkify

class Command(BaseCommand):
    help = 'Imports announcements from a WordPress export file.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=FileType('rb'))

    def handle(self, *args, **options):
        file = options['file']
        data = file.read()
        file.close()
        doc = BS(data, 'xml')
        items = doc.find_all('item')
        for item in items:
            status = item.status.get_text()

            # We only want published announcements
            if status != 'publish':
                continue

            title = item.title.get_text()
            description = markdown(item.encoded.get_text())
            description = linkify(description)
            slug = item.post_name.get_text()
            audience = keywords = []
            for cat in item.find_all('category', {'domain': 'audienceroles'}):
                audience.append(cat.get_text())

            for cat in item.find_all('category', {'domain': 'keywords'}):
                keywords.append(cat.get_text())

            # define variables
            start_date = end_date = contact_name = contact_email = contact_phone = url = None

            for meta in item.find_all('postmeta'):
                meta_key = meta.meta_key.get_text()
                meta_value = meta.meta_value.get_text()

                if meta_key == 'announcement_start_date':
                    start_date = datetime.strptime(meta_value, '%Y-%m-%d')

                if meta_key == 'announcement_end_date':
                    end_date = datetime.strptime(meta_value, '%Y-%m-%d')

                if meta_key == 'announcement_contact':
                    contact_name = meta_value

                if meta_key == 'announcement_posted_by':
                    posted_by = meta_value

                if meta_key == 'announcement_email':
                    contact_email = meta_value

                if meta_key == 'announcement_phone':
                    contact_phone = meta_value

                if meta_key == 'announcement_url':
                    url = meta_value

            try:
                new_item = Announcement.objects.create(
                    title = title,
                    description = description,
                    slug = slug,
                    keywords = ','.join(keywords),
                    start_date = start_date,
                    end_date = end_date,
                    contact_name = contact_name,
                    contact_email = contact_email,
                    contact_phone = contact_phone,
                    url = url,
                    posted_by = posted_by,
                    author_id = 1,
                    status='Publish'
                )

                new_item.save()

                audience_list = Audience.objects.all()

                for aud in audience:
                    try:
                        i = audience_list.get(name=aud)
                        new_item.audience.add(i)
                    except Audience.DoesNotExist:
                        continue


            except Exception, ex:
                print ex.message
                continue
