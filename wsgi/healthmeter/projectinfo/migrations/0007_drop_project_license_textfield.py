# Copyright 2017 Red Hat, Inc.
# License: GPLv3 or any later version

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.license'
        db.delete_column('projectinfo_project', 'license')


    def backwards(self, orm):
        # Adding field 'Project.license'
        db.add_column('projectinfo_project', 'license',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    models = {
        'projectinfo.license': {
            'Meta': {'object_name': 'License'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_osi_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'projectinfo.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'governance': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'has_contributor_agreement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'licenses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': "orm['projectinfo.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['projectinfo.Project']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'projectinfo.release': {
            'Meta': {'ordering': "('date', 'version')", 'unique_together': "(('project', 'version'),)", 'object_name': 'Release'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['projectinfo.Project']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['projectinfo']
