# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ListGenericManager'
        db.create_table('lists_listgenericmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lists', ['ListGenericManager'])

        # Adding model 'ListSuggestion'
        db.create_table('lists_listsuggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_vis', self.gf('django.db.models.fields.CharField')(default='private', max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('_short_url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('counter_followers', self.gf('fields.PositiveCounterField')(default=0, blank=True)),
        ))
        db.send_create_signal('lists', ['ListSuggestion'])

        # Adding model 'SuggestionInList'
        db.create_table('lists_suggestioninlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listsuggestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lists.ListSuggestion'])),
            ('suggestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Suggestion'])),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('lists', ['SuggestionInList'])

        # Adding unique constraint on 'SuggestionInList', fields ['listsuggestion', 'suggestion']
        db.create_unique('lists_suggestioninlist', ['listsuggestion_id', 'suggestion_id'])

        # Adding model 'ListFollower'
        db.create_table('lists_listfollower', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lists_followed', to=orm['auth.User'])),
            ('list_c_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='list_followers', to=orm['contenttypes.ContentType'])),
            ('list_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('lists', ['ListFollower'])

        # Adding unique constraint on 'ListFollower', fields ['user', 'list_c_type', 'list_id']
        db.create_unique('lists_listfollower', ['user_id', 'list_c_type_id', 'list_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ListFollower', fields ['user', 'list_c_type', 'list_id']
        db.delete_unique('lists_listfollower', ['user_id', 'list_c_type_id', 'list_id'])

        # Removing unique constraint on 'SuggestionInList', fields ['listsuggestion', 'suggestion']
        db.delete_unique('lists_suggestioninlist', ['listsuggestion_id', 'suggestion_id'])

        # Deleting model 'ListGenericManager'
        db.delete_table('lists_listgenericmanager')

        # Deleting model 'ListSuggestion'
        db.delete_table('lists_listsuggestion')

        # Deleting model 'SuggestionInList'
        db.delete_table('lists_suggestioninlist')

        # Deleting model 'ListFollower'
        db.delete_table('lists_listfollower')


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
            'slug': ('fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'populate_from': "['name', 'country']", 'overwrite': 'False', 'db_index': 'True'}),
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
        'events.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            '_short_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            '_vis': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '10'}),
            'counter_followers': ('fields.PositiveCounterField', [], {'default': '0', 'blank': 'True'}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ends': ('timezones.fields.LocalizedDateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_starts': ('timezones.fields.LocalizedDateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '170'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Place']"}),
            'slug': ('fields.AutoSlugField', [], {'populate_from': "['name', 'place']", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'_'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'lists.listfollower': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('user', 'list_c_type', 'list_id'),)", 'object_name': 'ListFollower'},
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'list_followers'", 'to': "orm['contenttypes.ContentType']"}),
            'list_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lists_followed'", 'to': "orm['auth.User']"})
        },
        'lists.listgenericmanager': {
            'Meta': {'object_name': 'ListGenericManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lists.listsuggestion': {
            'Meta': {'ordering': "['name', 'created', 'modified']", 'object_name': 'ListSuggestion'},
            '_short_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            '_vis': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '10'}),
            'counter_followers': ('fields.PositiveCounterField', [], {'default': '0', 'blank': 'True'}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'suggestions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['events.Suggestion']", 'through': "orm['lists.SuggestionInList']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'lists.suggestioninlist': {
            'Meta': {'unique_together': "(('listsuggestion', 'suggestion'),)", 'object_name': 'SuggestionInList'},
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listsuggestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.ListSuggestion']"}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'suggestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Suggestion']"})
        },
        'places.place': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Place'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            '_short_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': "orm['cities.City']"}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_places_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '232', 'blank': 'True'}),
            'google_places_reference': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '232', 'blank': 'True'}),
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

    complete_apps = ['lists']
