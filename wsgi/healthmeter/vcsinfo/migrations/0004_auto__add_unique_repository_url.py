# Copyright 2017 Red Hat, Inc.
# License: GPLv3 or any later version

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Repository', fields ['url']
        db.create_unique('vcsinfo_repository', ['url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repository', fields ['url']
        db.delete_unique('vcsinfo_repository', ['url'])


    models = {
        'participantinfo.participant': {
            'Meta': {'object_name': 'Participant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'vcsinfo.commit': {
            'Meta': {'unique_together': "(('repository', 'commit_id'),)", 'object_name': 'Commit'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['participantinfo.Participant']"}),
            'commit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commits'", 'to': "orm['vcsinfo.Repository']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'vcsinfo.repository': {
            'Meta': {'object_name': 'Repository'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repositories'", 'to': "orm['vcsinfo.Type']"}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10000'})
        },
        'vcsinfo.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['vcsinfo']