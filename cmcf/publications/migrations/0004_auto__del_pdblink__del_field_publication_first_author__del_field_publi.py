# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'pdblink'
        db.delete_table('publications_pdblink')

        # Deleting field 'Publication.first_author'
        db.delete_column('publication_index', 'first_author')

        # Deleting field 'Publication.volume'
        db.delete_column('publication_index', 'volume')

        # Deleting field 'Publication.pages'
        db.delete_column('publication_index', 'pages')

        # Deleting field 'Publication.issue'
        db.delete_column('publication_index', 'issue')

        # Removing M2M table for field PDBlink on 'Publication'
        db.delete_table('publication_index_PDBlink')


    def backwards(self, orm):
        
        # Adding model 'pdblink'
        db.create_table('publications_pdblink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('publications', ['pdblink'])

        # Adding field 'Publication.first_author'
        db.add_column('publication_index', 'first_author', self.gf('django.db.models.fields.TextField')(default="", max_length=150), keep_default=False)

        # Adding field 'Publication.volume'
        db.add_column('publication_index', 'volume', self.gf('django.db.models.fields.CharField')(default="", max_length=20, blank=True), keep_default=False)

        # Adding field 'Publication.pages'
        db.add_column('publication_index', 'pages', self.gf('django.db.models.fields.CharField')(default="", max_length=20, blank=True), keep_default=False)

        # Adding field 'Publication.issue'
        db.add_column('publication_index', 'issue', self.gf('django.db.models.fields.CharField')(default="", max_length=20, blank=True), keep_default=False)

        # Adding M2M table for field PDBlink on 'Publication'
        db.create_table('publication_index_PDBlink', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False)),
            ('pdblink', models.ForeignKey(orm['publications.pdblink'], null=False))
        ))
        db.create_unique('publication_index_PDBlink', ['publication_id', 'pdblink_id'])


    models = {
        'publications.journal': {
            'Meta': {'object_name': 'Journal'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'publications.publication': {
            'Meta': {'object_name': 'Publication', 'db_table': "'publication_index'"},
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'citation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Journal']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pdb_entries': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['publications']
