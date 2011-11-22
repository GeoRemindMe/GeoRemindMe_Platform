# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Place.street'
        db.delete_column('places_place', 'street')

        # Adding field 'Place.adress'
        db.add_column('places_place', 'adress', self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True), keep_default=False)

        # Changing field 'Place.slug'
        db.alter_column('places_place', 'slug', self.gf('webapp.site.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'_', populate_from=['name', 'city'], overwrite=False))

        # Adding unique constraint on 'Place', fields ['google_places_reference']
        db.create_unique('places_place', ['google_places_reference'])

        # Changing field 'City.slug'
        db.alter_column('places_city', 'slug', self.gf('webapp.site.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'_', populate_from=['name', 'region'], overwrite=False))

        # Changing field 'City.population'
        db.alter_column('places_city', 'population', self.gf('django.db.models.fields.IntegerField')(default=1))

        # Changing field 'Region.slug'
        db.alter_column('places_region', 'slug', self.gf('webapp.site.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'_', populate_from=['name', 'country'], overwrite=False))


    def backwards(self, orm):
        
        # Removing unique constraint on 'Place', fields ['google_places_reference']
        db.delete_unique('places_place', ['google_places_reference'])

        # Adding field 'Place.street'
        db.add_column('places_place', 'street', self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True), keep_default=False)

        # Deleting field 'Place.adress'
        db.delete_column('places_place', 'adress')

        # Changing field 'Place.slug'
        db.alter_column('places_place', 'slug', self.gf('webapp.site.fields.AutoSlugField')(populate_from=['name', 'city'], allow_duplicates=False, max_length=50, separator=u'-', overwrite=False))

        # Changing field 'City.slug'
        db.alter_column('places_city', 'slug', self.gf('webapp.site.fields.AutoSlugField')(populate_from=['name', 'region'], allow_duplicates=False, max_length=50, separator=u'-', overwrite=False))

        # Changing field 'City.population'
        db.alter_column('places_city', 'population', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Region.slug'
        db.alter_column('places_region', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=150))


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
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'blank': 'True', 'to': "orm['places.Region']"}),
            'slug': ('webapp.site.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'region']", 'overwrite': 'False', 'db_index': 'True'})
        },
        'places.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        'places.place': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Place'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            '_short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'adress': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['places.City']"}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_places_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '232', 'blank': 'True'}),
            'google_places_reference': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '232', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'slug': ('webapp.site.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'city']", 'overwrite': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['auth.User']"})
        },
        'places.region': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Region'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': "orm['places.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('webapp.site.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'country']", 'overwrite': 'False', 'db_index': 'True'})
        }
    }

    complete_apps = ['places']
