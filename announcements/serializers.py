from rest_framework import serializers
from announcements.models import *
from taggit.models import *
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')

class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ('name',)

class AnnouncementSerializer(serializers.ModelSerializer):
    audience = AudienceSerializer(many=True)
    keywords = TagListSerializerField()

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'description', 'audience', 'keywords', 'start_date', 'end_date', 'url', 'contact_name', 'contact_phone', 'contact_email', 'posted_by', 'status')

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
