# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'WebStatus.week'
        db.add_column('scheduler_webstatus', 'week', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 9, 30)), keep_default=False)

        # Adding unique constraint on 'WebStatus', fields ['week', 'year']
        db.create_unique('scheduler_webstatus', ['week', 'year'])


    def backwards(self, orm):
        
        # Deleting field 'WebStatus.week'
        db.delete_column('scheduler_webstatus', 'week')

        # Removing unique constraint on 'WebStatus', fields ['week', 'year']
        db.delete_unique('scheduler_webstatus', ['week', 'year'])


    models = {
        'scheduler.beamline': {
            'Meta': {'object_name': 'Beamline'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'scheduler.mode': {
            'Meta': {'object_name': 'Mode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'scheduler.oncall': {
            'Meta': {'unique_together': "(('local_contact', 'date'),)", 'object_name': 'OnCall'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.SupportPerson']"})
        },
        'scheduler.stat': {
            'Meta': {'unique_together': "(('mode', 'start_date', 'first_shift'), ('mode', 'end_date', 'last_shift'))", 'object_name': 'Stat'},
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'first_shift': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_shift': ('django.db.models.fields.IntegerField', [], {}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'scheduler.supportperson': {
            'Meta': {'unique_together': "(('first_name', 'last_name', 'email'),)", 'object_name': 'SupportPerson'},
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.visit': {
            'Meta': {'unique_together': "(('beamline', 'start_date', 'first_shift'), ('beamline', 'end_date', 'last_shift'))", 'object_name': 'Visit'},
            'beamline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Beamline']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'first_shift': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_shift': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'scheduler.webstatus': {
            'Meta': {'unique_together': "(('year', 'week'),)", 'object_name': 'WebStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('jsonfield.JSONField', [], {}),
            'week': ('django.db.models.fields.DateField', [], {}),
            'year': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['scheduler']
