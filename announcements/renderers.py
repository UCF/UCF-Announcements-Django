"""
Provides XML rendering support.
"""
from __future__ import unicode_literals

from django.utils import six
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text
from rest_framework_xml.renderers import XMLRenderer

class AnnouncementXMLRenderer(XMLRenderer):
    root_tag_name = 'announcements'
    item_tag_name = 'announcement'

    def render(self, data, media_type=None, renderer_context=None):
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_tag_name, {})

        super(AnnouncementXMLRenderer, self)._to_xml(xml, data)

        xml.endElement(self.root_tag_name)
        xml.endDocument()
        return stream.getvalue()
