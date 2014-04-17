# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Classroom'
        db.create_table(u'project_share_classroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teacher_classrooms', to=orm['project_share.ExtendedUser'])),
        ))
        db.send_create_signal(u'project_share', ['Classroom'])

        # Adding M2M table for field students on 'Classroom'
        m2m_table_name = db.shorten_name(u'project_share_classroom_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classroom', models.ForeignKey(orm[u'project_share.classroom'], null=False)),
            ('extendeduser', models.ForeignKey(orm[u'project_share.extendeduser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classroom_id', 'extendeduser_id'])

        # Adding model 'Approval'
        db.create_table(u'project_share_approval', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project_share.Project'], unique=True)),
            ('when_requested', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project_share.ExtendedUser'], null=True, blank=True)),
        ))
        db.send_create_signal(u'project_share', ['Approval'])

        # Adding model 'Application'
        db.create_table(u'project_share_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('codebase_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'project_share', ['Application'])

        # Adding model 'Project'
        db.create_table(u'project_share_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project_share.Application'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project_share.ExtendedUser'])),
            ('project', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('screenshot', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'project_share', ['Project'])

        # Adding unique constraint on 'Project', fields ['name', 'owner']
        db.create_unique(u'project_share_project', ['name', 'owner_id'])

        # Adding unique constraint on 'Project', fields ['project', 'owner']
        db.create_unique(u'project_share_project', ['project', 'owner_id'])

        # Adding unique constraint on 'Project', fields ['screenshot', 'owner']
        db.create_unique(u'project_share_project', ['screenshot', 'owner_id'])

        # Adding model 'ExtendedUser'
        db.create_table(u'project_share_extendeduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'project_share', ['ExtendedUser'])

        # Adding M2M table for field groups on 'ExtendedUser'
        m2m_table_name = db.shorten_name(u'project_share_extendeduser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('extendeduser', models.ForeignKey(orm[u'project_share.extendeduser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['extendeduser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'ExtendedUser'
        m2m_table_name = db.shorten_name(u'project_share_extendeduser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('extendeduser', models.ForeignKey(orm[u'project_share.extendeduser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['extendeduser_id', 'permission_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Project', fields ['screenshot', 'owner']
        db.delete_unique(u'project_share_project', ['screenshot', 'owner_id'])

        # Removing unique constraint on 'Project', fields ['project', 'owner']
        db.delete_unique(u'project_share_project', ['project', 'owner_id'])

        # Removing unique constraint on 'Project', fields ['name', 'owner']
        db.delete_unique(u'project_share_project', ['name', 'owner_id'])

        # Deleting model 'Classroom'
        db.delete_table(u'project_share_classroom')

        # Removing M2M table for field students on 'Classroom'
        db.delete_table(db.shorten_name(u'project_share_classroom_students'))

        # Deleting model 'Approval'
        db.delete_table(u'project_share_approval')

        # Deleting model 'Application'
        db.delete_table(u'project_share_application')

        # Deleting model 'Project'
        db.delete_table(u'project_share_project')

        # Deleting model 'ExtendedUser'
        db.delete_table(u'project_share_extendeduser')

        # Removing M2M table for field groups on 'ExtendedUser'
        db.delete_table(db.shorten_name(u'project_share_extendeduser_groups'))

        # Removing M2M table for field user_permissions on 'ExtendedUser'
        db.delete_table(db.shorten_name(u'project_share_extendeduser_user_permissions'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'project_share.application': {
            'Meta': {'object_name': 'Application'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'codebase_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'project_share.approval': {
            'Meta': {'object_name': 'Approval'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project_share.ExtendedUser']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['project_share.Project']", 'unique': 'True'}),
            'when_requested': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'project_share.classroom': {
            'Meta': {'object_name': 'Classroom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'student_classrooms'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['project_share.ExtendedUser']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teacher_classrooms'", 'to': u"orm['project_share.ExtendedUser']"})
        },
        u'project_share.extendeduser': {
            'Meta': {'object_name': 'ExtendedUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'project_share.project': {
            'Meta': {'unique_together': "(('name', 'owner'), ('project', 'owner'), ('screenshot', 'owner'))", 'object_name': 'Project'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project_share.Application']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project_share.ExtendedUser']"}),
            'project': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'screenshot': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'secretballot.vote': {
            'Meta': {'unique_together': "(('token', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['project_share']