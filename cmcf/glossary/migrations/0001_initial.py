# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Term'
        db.create_table('glossary_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('glossary', ['Term'])

        # Adding model 'Synonym'
        db.create_table('glossary_synonym', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonyms', to=orm['glossary.Term'])),
        ))
        db.send_create_signal('glossary', ['Synonym'])


    def backwards(self, orm):
        
        # Deleting model 'Term'
        db.delete_table('glossary_term')

        # Deleting model 'Synonym'
        db.delete_table('glossary_synonym')


    models = {
        'glossary.synonym': {
            'Meta': {'object_name': 'Synonym'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': "orm['glossary.Term']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'glossary.term': {
            'Meta': {'object_name': 'Term'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['glossary']
