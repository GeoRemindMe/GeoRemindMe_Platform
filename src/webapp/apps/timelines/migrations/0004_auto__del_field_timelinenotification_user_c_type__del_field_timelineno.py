# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'TimelineNotification.user_c_type'
        db.delete_column('timelines_timelinenotification', 'user_c_type_id')

        # Deleting field 'TimelineNotification.user_id'
        db.delete_column('timelines_timelinenotification', 'user_id')

        # Adding field 'TimelineNotification.actor_c_type'
        db.add_column('timelines_timelinenotification', 'actor_c_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='timelinenotifications', to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'TimelineNotification.actor_id'
        db.add_column('timelines_timelinenotification', 'actor_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1), keep_default=False)

        # Adding field 'TimelineNotification.modified'
        db.add_column('timelines_timelinenotification', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, default=datetime.datetime(2012, 3, 1, 13, 25, 18, 336684), blank=True), keep_default=False)

        # Adding field 'TimelineFollower.modified'
        db.add_column('timelines_timelinefollower', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, default=datetime.datetime(2012, 3, 1, 13, 25, 24, 377460), blank=True), keep_default=False)

        # Adding field 'Follower.modified'
        db.add_column('timelines_follower', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True, default=datetime.datetime(2012, 3, 1, 13, 25, 32, 250159), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'TimelineNotification.user_c_type'
        raise RuntimeError("Cannot reverse this migration. 'TimelineNotification.user_c_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TimelineNotification.user_id'
        raise RuntimeError("Cannot reverse this migration. 'TimelineNotification.user_id' and its values cannot be restored.")

        # Deleting field 'TimelineNotification.actor_c_type'
        db.delete_column('timelines_timelinenotification', 'actor_c_type_id')

        # Deleting field 'TimelineNotification.actor_id'
        db.delete_column('timelines_timelinenotification', 'actor_id')

        # Deleting field 'TimelineNotification.modified'
        db.delete_column('timelines_timelinenotification', 'modified')

        # Deleting field 'TimelineFollower.modified'
        db.delete_column('timelines_timelinefollower', 'modified')

        # Deleting field 'Follower.modified'
        db.delete_column('timelines_follower', 'modified')


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
        'timelines.follower': {
            'Meta': {'unique_together': "(('follower_c_type', 'follower_id', 'followee_c_type', 'followee_id'),)", 'object_name': 'Follower'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'followee_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followers'", 'to': "orm['contenttypes.ContentType']"}),
            'followee_id': ('django.db.models.fields.IntegerField', [], {}),
            'follower_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followings'", 'to': "orm['contenttypes.ContentType']"}),
            'follower_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'timelines.notificationsettings': {
            'Meta': {'object_name': 'NotificationSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_account': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'notification_invitation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'notification_suggestion': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'timelines.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'actor_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_id': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'msg_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'objetive_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'objetive_id': ('django.db.models.fields.IntegerField', [], {}),
            'result_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'result_id': ('django.db.models.fields.IntegerField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'timelines.timelinefollower': {
            'Meta': {'unique_together': "(('timeline', 'follower_c_type', 'follower_id'),)", 'object_name': 'TimelineFollower'},
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follower_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinefollowings'", 'to': "orm['contenttypes.ContentType']"}),
            'follower_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinefollowers'", 'to': "orm['timelines.Timeline']"})
        },
        'timelines.timelinenotification': {
            'Meta': {'ordering': "['-created']", 'object_name': 'TimelineNotification'},
            'actor_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinenotifications'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinenotifications'", 'to': "orm['timelines.Timeline']"})
        }
    }

    complete_apps = ['timelines']
