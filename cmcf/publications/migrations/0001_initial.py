# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Journal'
        db.create_table('publications_journal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('publications', ['Journal'])

        # Adding model 'pdblink'
        db.create_table('publications_pdblink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('publications', ['pdblink'])

        # Adding model 'Publication'
        db.create_table('publication_index', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, db_index=True)),
            ('first_author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Journal'])),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('issue', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('publish', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('publications', ['Publication'])

        # Adding M2M table for field PDBlink on 'Publication'
        db.create_table('publication_index_PDBlink', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False)),
            ('pdblink', models.ForeignKey(orm['publications.pdblink'], null=False))
        ))
        db.create_unique('publication_index_PDBlink', ['publication_id', 'pdblink_id'])


    def backwards(self, orm):
        
        # Deleting model 'Journal'
        db.delete_table('publications_journal')

        # Deleting model 'pdblink'
        db.delete_table('publications_pdblink')

        # Deleting model 'Publication'
        db.delete_table('publication_index')

        # Removing M2M table for field PDBlink on 'Publication'
        db.delete_table('publication_index_PDBlink')


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
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Journal']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['publications']
