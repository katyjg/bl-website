# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Beamline'
        db.create_table('scheduler_beamline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('scheduler', ['Beamline'])

        # Adding model 'SupportPerson'
        db.create_table('scheduler_supportperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('scheduler', ['SupportPerson'])

        # Adding unique constraint on 'SupportPerson', fields ['first_name', 'last_name', 'email']
        db.create_unique('scheduler_supportperson', ['first_name', 'last_name', 'email'])

        # Adding model 'Visit'
        db.create_table('scheduler_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('beamline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Beamline'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('first_shift', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('last_shift', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('scheduler', ['Visit'])

        # Adding unique constraint on 'Visit', fields ['beamline', 'start_date', 'first_shift']
        db.create_unique('scheduler_visit', ['beamline_id', 'start_date', 'first_shift'])

        # Adding unique constraint on 'Visit', fields ['beamline', 'end_date', 'last_shift']
        db.create_unique('scheduler_visit', ['beamline_id', 'end_date', 'last_shift'])

        # Adding model 'OnCall'
        db.create_table('scheduler_oncall', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.SupportPerson'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('scheduler', ['OnCall'])

        # Adding unique constraint on 'OnCall', fields ['local_contact', 'date']
        db.create_unique('scheduler_oncall', ['local_contact_id', 'date'])

        # Adding model 'WebStatus'
        db.create_table('scheduler_webstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.CharField')(default='', max_length=15)),
            ('status1', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('status2', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('status3', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
        ))
        db.send_create_signal('scheduler', ['WebStatus'])

        # Adding unique constraint on 'WebStatus', fields ['date']
        db.create_unique('scheduler_webstatus', ['date'])

        # Adding model 'Stat'
        db.create_table('scheduler_stat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('first_shift', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('last_shift', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('scheduler', ['Stat'])

        # Adding unique constraint on 'Stat', fields ['mode', 'start_date', 'first_shift']
        db.create_unique('scheduler_stat', ['mode', 'start_date', 'first_shift'])

        # Adding unique constraint on 'Stat', fields ['mode', 'end_date', 'last_shift']
        db.create_unique('scheduler_stat', ['mode', 'end_date', 'last_shift'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Stat', fields ['mode', 'end_date', 'last_shift']
        db.delete_unique('scheduler_stat', ['mode', 'end_date', 'last_shift'])

        # Removing unique constraint on 'Stat', fields ['mode', 'start_date', 'first_shift']
        db.delete_unique('scheduler_stat', ['mode', 'start_date', 'first_shift'])

        # Removing unique constraint on 'WebStatus', fields ['date']
        db.delete_unique('scheduler_webstatus', ['date'])

        # Removing unique constraint on 'OnCall', fields ['local_contact', 'date']
        db.delete_unique('scheduler_oncall', ['local_contact_id', 'date'])

        # Removing unique constraint on 'Visit', fields ['beamline', 'end_date', 'last_shift']
        db.delete_unique('scheduler_visit', ['beamline_id', 'end_date', 'last_shift'])

        # Removing unique constraint on 'Visit', fields ['beamline', 'start_date', 'first_shift']
        db.delete_unique('scheduler_visit', ['beamline_id', 'start_date', 'first_shift'])

        # Removing unique constraint on 'SupportPerson', fields ['first_name', 'last_name', 'email']
        db.delete_unique('scheduler_supportperson', ['first_name', 'last_name', 'email'])

        # Deleting model 'Beamline'
        db.delete_table('scheduler_beamline')

        # Deleting model 'SupportPerson'
        db.delete_table('scheduler_supportperson')

        # Deleting model 'Visit'
        db.delete_table('scheduler_visit')

        # Deleting model 'OnCall'
        db.delete_table('scheduler_oncall')

        # Deleting model 'WebStatus'
        db.delete_table('scheduler_webstatus')

        # Deleting model 'Stat'
        db.delete_table('scheduler_stat')


    models = {
        'scheduler.beamline': {
            'Meta': {'object_name': 'Beamline'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'Meta': {'unique_together': "(('date',),)", 'object_name': 'WebStatus'},
            'date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'status2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'status3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        }
    }

    complete_apps = ['scheduler']
