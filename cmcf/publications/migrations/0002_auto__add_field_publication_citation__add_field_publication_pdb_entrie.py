# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Publication.citation'
        db.add_column('publication_index', 'citation', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Adding field 'Publication.pdb_entries'
        db.add_column('publication_index', 'pdb_entries', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Changing field 'Publication.first_author'
        db.alter_column('publication_index', 'first_author', self.gf('django.db.models.fields.TextField')(max_length=150))

        # Changing field 'Publication.authors'
        db.alter_column('publication_index', 'authors', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True))

        # Changing field 'Publication.title'
        db.alter_column('publication_index', 'title', self.gf('django.db.models.fields.TextField')(max_length=200))


    def backwards(self, orm):
        
        # Deleting field 'Publication.citation'
        db.delete_column('publication_index', 'citation')

        # Deleting field 'Publication.pdb_entries'
        db.delete_column('publication_index', 'pdb_entries')

        # Changing field 'Publication.first_author'
        db.alter_column('publication_index', 'first_author', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Changing field 'Publication.authors'
        db.alter_column('publication_index', 'authors', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True))

        # Changing field 'Publication.title'
        db.alter_column('publication_index', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))


    models = {
        'publications.journal': {
            'Meta': {'object_name': 'Journal'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'publications.pdblink': {
            'Meta': {'object_name': 'pdblink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'publications.publication': {
            'Meta': {'object_name': 'Publication', 'db_table': "'publication_index'"},
            'PDBlink': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['publications.pdblink']", 'symmetrical': 'False', 'blank': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'citation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_author': ('django.db.models.fields.TextField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Journal']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'pdb_entries': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['publications']
