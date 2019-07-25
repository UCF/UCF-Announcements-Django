# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 15:16


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=128, unique=True)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('url', models.URLField(blank=True, null=True)),
                ('contact_name', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('contact_email', models.CharField(max_length=100)),
                ('posted_by', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Publish', 'Publish')], max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='audience',
            field=models.ManyToManyField(related_name='announcements', to='announcements.Audience'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announcement',
            name='keywords',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
