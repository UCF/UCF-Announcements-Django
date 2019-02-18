from rest_framework import serializers
from announcements.models import *
from taggit.models import *
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from drf_dynamic_fields import DynamicFieldsMixin
import warnings

# Mixins
class DynamicFieldSetMixin(DynamicFieldsMixin):
    """
    Expands the functionality of the Dynamic Fields Mixin
    """
    def __init__(self, *args, **kwargs):
        super(DynamicFieldSetMixin, self).__init__(*args, **kwargs)

        if hasattr(self.Meta, "fieldsets"):
            self.fieldsets = self.Meta.fieldsets
        else:
            self.fieldsets = None

    @property
    def fields(self):
        # Do initial fields logic
        fields = super(DynamicFieldSetMixin, self).fields

        # Check for request object in context
        try:
            request = self.context['request']
        except KeyError:
            warnings.warn('Context does not have access to request')
            return fields

        # Check for query_params within GET param
        params = getattr(
            request, 'query_params', getattr(request, 'GET', None)
        )
        if params is None:
            warnings.warn('Request object does not contain query parameters')

        # Get fieldset
        try:
            fieldset = params.get('fieldset', None)
        except AttributeError:
            fieldset = None
            return fields

        if self.fieldsets and fieldset in self.fieldsets:
            existing = set(fields.keys())
            allowed = self.fieldsets[fieldset]

            for field in existing:

                if field not in allowed:
                    fields.pop(field, None)

        return fields

# Model Serializers
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')

class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ('name',)

class AnnouncementSerializer(DynamicFieldSetMixin, serializers.ModelSerializer):
    audience = AudienceSerializer(many=True)
    keywords = TagListSerializerField()

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'description', 'audience', 'keywords', 'start_date', 'end_date', 'url', 'contact_name', 'contact_phone', 'contact_email', 'posted_by', 'status', 'slug', 'permalink')
        fieldsets = {
            "options": "id,title",
        }

    def perform_create(self, validated_data):
        serializer.save(author=self.request.user)

    def create(self, validated_data):
        # Handle keywords and audience
        keywords = validated_data.pop('keywords')
        audiences = validated_data.pop('audience')
        validated_data['status'] = "Pending"

        announcement = Announcement.objects.create(**validated_data)

        for keyword in keywords:
            announcement.keywords.add(keyword)

        for aud in audiences:
            audience, created = Audience.objects.get_or_create(**aud)
            audience.announcements.add(announcement)

        audience.save()

        return announcement
