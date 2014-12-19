# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from django.db import models, migrations
import project_share.models
import taggit.managers
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('school', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255, verbose_name=b'State or Province')),
                ('country', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('teacher', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('version', models.CharField(max_length=10, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('codebase_url', models.CharField(max_length=255, null=True, blank=True)),
                ('class_name', models.CharField(max_length=255, null=True, blank=True)),
                ('more_info_url', models.URLField(null=True, blank=True)),
                ('application_file', models.FileField(null=True, upload_to=project_share.models.application_application, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=100)),
                ('title', models.TextField()),
                ('html_data', models.TextField(null=True, blank=True)),
                ('application', models.ForeignKey(to='project_share.Application')),
                ('parent', models.ForeignKey(blank=True, to='project_share.ApplicationContext', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationDemo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField(default=1000, blank=True)),
                ('zipfile', models.FileField(upload_to=project_share.models.application_application_demo)),
                ('application', models.ForeignKey(to='project_share.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_requested', models.DateTimeField(auto_now_add=True)),
                ('when_updated', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('students', models.ManyToManyField(related_name='student_classrooms', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('teacher', models.ForeignKey(related_name='teacher_classrooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f', models.FileField(upload_to=b'files/%Y-%m-%d/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('thumbnail', models.FileField(upload_to=project_share.models.application_application_goal)),
                ('image', models.FileField(upload_to=project_share.models.application_application_goal)),
                ('application', models.ForeignKey(to='project_share.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('lib_file', models.FileField(upload_to=project_share.models.module_library)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('module_file', models.FileField(null=True, upload_to=project_share.models.module_module, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('application', models.ForeignKey(to='project_share.Application')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='project_share.Project', null=True)),
                ('project', models.ForeignKey(related_name='+', blank=True, to='project_share.FileUpload', null=True)),
                ('screenshot', models.ForeignKey(related_name='+', blank=True, to='project_share.FileUpload', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='approval',
            name='project',
            field=models.OneToOneField(to='project_share.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='application_type',
            field=models.ForeignKey(blank=True, to='project_share.ApplicationType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='module',
            field=models.ForeignKey(blank=True, to='project_share.Module', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]

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