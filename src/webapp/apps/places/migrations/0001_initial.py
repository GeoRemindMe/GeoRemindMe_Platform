# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Place'
        db.create_table('places_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'_', blank=True, populate_from=['name', 'city'], overwrite=False, db_index=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(related_name='places', to=orm['cities.City'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='places', to=orm['auth.User'])),
            ('google_places_reference', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('google_places_id', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=512, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('_short_url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('places', ['Place'])


    def backwards(self, orm):
        
        # Deleting model 'Place'
        db.delete_table('places_place')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cities.city': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'City'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'blank': 'True', 'to': "orm['cities.Region']"}),
            'slug': ('fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'region']", 'overwrite': 'False', 'db_index': 'True'})
        },
        'cities.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'slug': ('fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False', 'db_index': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        'cities.region': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Region'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': "orm['cities.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'country']", 'overwrite': 'False', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'places.place': {
            'Meta': {'object_name': 'Place'},
            '_short_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['cities.City']"}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_places_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'google_places_reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'slug': ('fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'city']", 'overwrite': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['places']
