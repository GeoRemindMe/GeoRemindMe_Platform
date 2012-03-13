# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'TimelineNotification.created'
        db.alter_column('timelines_timelinenotification', 'created', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'TimelineNotification.modified'
        db.alter_column('timelines_timelinenotification', 'modified', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now=True))

        # Changing field 'Timeline.created'
        db.alter_column('timelines_timeline', 'created', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'Timeline.modified'
        db.alter_column('timelines_timeline', 'modified', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now=True))

        # Changing field 'TimelineFollower.created'
        db.alter_column('timelines_timelinefollower', 'created', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'TimelineFollower.modified'
        db.alter_column('timelines_timelinefollower', 'modified', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now=True))

        # Changing field 'Follower.created'
        db.alter_column('timelines_follower', 'created', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'Follower.modified'
        db.alter_column('timelines_follower', 'modified', self.gf('modules.timezones.fields.LocalizedDateTimeField')(auto_now=True))


    def backwards(self, orm):
        
        # Changing field 'TimelineNotification.created'
        db.alter_column('timelines_timelinenotification', 'created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'TimelineNotification.modified'
        db.alter_column('timelines_timelinenotification', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True))

        # Changing field 'Timeline.created'
        db.alter_column('timelines_timeline', 'created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'Timeline.modified'
        db.alter_column('timelines_timeline', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True))

        # Changing field 'TimelineFollower.created'
        db.alter_column('timelines_timelinefollower', 'created', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now_add=True))

        # Changing field 'TimelineFollower.modified'
        db.alter_column('timelines_timelinefollower', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True))

        # Changing field 'Follower.created'
        db.alter_column('timelines_follower', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Follower.modified'
        db.alter_column('timelines_follower', 'modified', self.gf('timezones.fields.LocalizedDateTimeField')(auto_now=True))


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
            'created': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'followee_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followers'", 'to': "orm['contenttypes.ContentType']"}),
            'followee_id': ('django.db.models.fields.IntegerField', [], {}),
            'follower_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followings'", 'to': "orm['contenttypes.ContentType']"}),
            'follower_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        'timelines.timelinefollower': {
            'Meta': {'unique_together': "(('timeline', 'follower_c_type', 'follower_id'),)", 'object_name': 'TimelineFollower'},
            'created': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follower_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'follower_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinefollowers'", 'to': "orm['timelines.Timeline']"})
        },
        'timelines.timelinenotification': {
            'Meta': {'ordering': "['-created']", 'object_name': 'TimelineNotification'},
            'actor_c_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinenotifications'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('modules.timezones.fields.LocalizedDateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelinenotifications'", 'to': "orm['timelines.Timeline']"})
        }
    }

    complete_apps = ['timelines']
