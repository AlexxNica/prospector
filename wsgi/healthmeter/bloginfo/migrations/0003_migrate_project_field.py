# Copyright 2017 Red Hat, Inc.
# License: GPLv3 or any later version

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import itertools

class Migration(DataMigration):

    def forwards(self, orm):
        Blog = orm['bloginfo.Blog']

        # Copy all of its own blogs...
        blogs_qs = Blog.objects.select_related('project').order_by('rss_url')
        blogs = itertools.groupby(list(blogs_qs), lambda b: b.rss_url)

        for rss_url, blog_items in blogs:
            # take the first one
            blog_iter = iter(blog_items)
            main_blog = next(blog_iter)
            main_blog.projects.add(main_blog.project)

            for blog in blog_iter:
                main_blog.projects.add(blog.project)
                blog.delete()

    def backwards(self, orm):
        Blog = orm['bloginfo.Blog']
        blogs_qs = Blog.objects.prefetch_related('projects')

        for blog in list(blogs_qs):
            try:
                it = iter(blog.projects.all())
                blog.project = next(it)
                blog.save()
                for project in blog.projects.all():
                    if Blog.objects.filter(rss_url=blog.rss_url,
                                           project=project).exists():
                        continue

                    blog.id = None
                    blog.project = project
                    blog.save()

            except StopIteration:
                pass

    models = {
        u'bloginfo.blog': {
            'Meta': {'object_name': 'Blog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'project': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['projectinfo.Project']", 'null': 'True'}),
            'projects': ('mptt.fields.TreeManyToManyField', [], {'related_name': "'blogs'", 'symmetrical': 'False', 'to': u"orm['projectinfo.Project']"}),
            'rss_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255'})
        },
        u'bloginfo.post': {
            'Meta': {'unique_together': "(('blog', 'guid'),)", 'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['participantinfo.Participant']", 'null': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['bloginfo.Blog']"}),
            'guid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        u'participantinfo.participant': {
            'Meta': {'object_name': 'Participant'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projectinfo.businessunit': {
            'Meta': {'object_name': 'BusinessUnit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'projectinfo.license': {
            'Meta': {'object_name': 'License'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_osi_approved': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        u'projectinfo.project': {
            'Meta': {'object_name': 'Project'},
            'business_unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'to': u"orm['projectinfo.BusinessUnit']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'governance': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'has_contributor_agreement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_wip': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'licenses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['projectinfo.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['projectinfo.Project']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bloginfo']
    symmetrical = True