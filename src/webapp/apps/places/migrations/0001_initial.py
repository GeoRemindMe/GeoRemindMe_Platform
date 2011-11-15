# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('places_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
            ('continent', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('tld', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal('places', ['Country'])

        # Adding model 'Region'
        db.create_table('places_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regions', to=orm['places.Country'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('places', ['Region'])

        # Adding model 'City'
        db.create_table('places_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cities', to=orm['places.Region'])),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('places', ['City'])

        # Adding model 'Place'
        db.create_table('places_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(related_name='places', to=orm['places.City'])),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('num', self.gf('django.db.models.fields.IntegerField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='places', to=orm['auth.User'])),
            ('google_places_reference', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=232, blank=True)),
            ('google_places_id', self.gf('django.db.models.fields.CharField')(max_length=232, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('places', ['Place'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('places_country')

        # Deleting model 'Region'
        db.delete_table('places_region')

        # Deleting model 'City'
        db.delete_table('places_city')

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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'places.city': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'City'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['places.Region']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'places.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'tld': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        'places.place': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Place'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['places.City']"}),
            'google_places_id': ('django.db.models.fields.CharField', [], {'max_length': '232', 'blank': 'True'}),
            'google_places_reference': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '232', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['auth.User']"})
        },
        'places.region': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Region'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': "orm['places.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['places']
