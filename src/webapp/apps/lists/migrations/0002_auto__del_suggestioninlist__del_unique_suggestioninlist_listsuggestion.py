# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'ListFollower', fields ['user', 'list_c_type', 'list_id']
        db.delete_unique('lists_listfollower', ['user_id', 'list_c_type_id', 'list_id'])

        # Removing unique constraint on 'SuggestionInList', fields ['listsuggestion', 'suggestion']
        db.delete_unique('lists_suggestioninlist', ['listsuggestion_id', 'suggestion_id'])

        # Deleting model 'SuggestionInList'
        db.delete_table('lists_suggestioninlist')

        # Deleting model 'ListGenericManager'
        db.delete_table('lists_listgenericmanager')

        # Deleting model 'ListFollower'
        db.delete_table('lists_listfollower')

        # Deleting model 'ListSuggestion'
        db.delete_table('lists_listsuggestion')

        # Adding model 'List'
        db.create_table('lists_list', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_vis', self.gf('django.db.models.fields.CharField')(default='private', max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('lists', ['List'])

        # Adding model 'ListRecipient'
        db.create_table('lists_listrecipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('in_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipients', to=orm['lists.List'])),
            ('recipient_c_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['contenttypes.ContentType'])),
            ('recipient_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('lists', ['ListRecipient'])


    def backwards(self, orm):
        
        # Adding model 'SuggestionInList'
        db.create_table('lists_suggestioninlist', (
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
            ('suggestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Suggestion'])),
            ('listsuggestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lists.ListSuggestion'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lists', ['SuggestionInList'])

        # Adding unique constraint on 'SuggestionInList', fields ['listsuggestion', 'suggestion']
        db.create_unique('lists_suggestioninlist', ['listsuggestion_id', 'suggestion_id'])

        # Adding model 'ListGenericManager'
        db.create_table('lists_listgenericmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lists', ['ListGenericManager'])

        # Adding model 'ListFollower'
        db.create_table('lists_listfollower', (
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
            ('list_c_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='list_followers', to=orm['contenttypes.ContentType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lists_followed', to=orm['auth.User'])),
            ('list_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lists', ['ListFollower'])

        # Adding unique constraint on 'ListFollower', fields ['user', 'list_c_type', 'list_id']
        db.create_unique('lists_listfollower', ['user_id', 'list_c_type_id', 'list_id'])

        # Adding model 'ListSuggestion'
        db.create_table('lists_listsuggestion', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('_vis', self.gf('django.db.models.fields.CharField')(default='private', max_length=10)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True, blank=True)),
            ('counter_followers', self.gf('fields.PositiveCounterField')(default=0, blank=True)),
            ('modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, blank=True)),
            ('_short_url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
        ))
        db.send_create_signal('lists', ['ListSuggestion'])

        # Deleting model 'List'
        db.delete_table('lists_list')

        # Deleting model 'ListRecipient'
        db.delete_table('lists_listrecipient')


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
        'lists.list': {
            'Meta': {'object_name': 'List'},
            '_vis': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '10'}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'lists.listrecipient': {
            'Meta': {'object_name': 'ListRecipient'},
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipients'", 'to': "orm['lists.List']"}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'recipient_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'recipient_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['lists']
