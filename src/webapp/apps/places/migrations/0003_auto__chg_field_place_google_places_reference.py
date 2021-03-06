# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Place.google_places_reference'
        db.alter_column('places_place', 'google_places_reference', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512))


    def backwards(self, orm):
        
        # Changing field 'Place.google_places_reference'
        db.alter_column('places_place', 'google_places_reference', self.gf('django.db.models.fields.CharField')(max_length=1024, unique=True))


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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['cities.City']"}),
            'created': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_places_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'google_places_reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'modified': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'slug': ('fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'city']", 'overwrite': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['auth.User']"})
        },
        'timelines.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'actor_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_id': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'msg_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'objetive_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'objetive_id': ('django.db.models.fields.IntegerField', [], {}),
            'result_c_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'result_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'voty.vote': {
            'Meta': {'unique_together': "(['user', 'target_c_type', 'target_id'],)", 'object_name': 'Vote'},
            'created': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'target_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'target_id': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['places']
