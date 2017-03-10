'''Project_Share Signals'''

from django_comments_xtd.models import XtdComment
from django_teams.models import Ownership
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from project_share.models import Approval, Project


@receiver(post_save, sender=Approval)
def approval_handler(instance):
    '''Approval Handler'''
    if instance.approved_by is not None:
        instance.project.approved = True
        instance.project.save()


@receiver(post_save, sender=XtdComment)
def approval_comment(instance, created):
    '''Approval Comment'''
    if created is True:
        instance.is_public = False
        instance.save()


@receiver(post_save, sender=Ownership)
def approval_comment(instance):
    '''Approval Comment'''
    if instance.content_type == \
            ContentType.objects.get(
                app_label="project_share", model="project") \
            and instance.approved is True:
        project = Project.objects.get(pk=instance.object_id)
        project.approved = True
        project.save()
