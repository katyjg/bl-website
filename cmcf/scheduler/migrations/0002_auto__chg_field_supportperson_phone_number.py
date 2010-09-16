# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'SupportPerson.phone_number'
        db.alter_column('scheduler_supportperson', 'phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True))


    def backwards(self, orm):
        
        # Changing field 'SupportPerson.phone_number'
        db.alter_column('scheduler_supportperson', 'phone_number', self.gf('django.db.models.fields.CharField')(max_length=20))


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
        }
    }

    complete_apps = ['scheduler']
