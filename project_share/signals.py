"""When approval is changed it updates projects accordingly."""
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_comments_xtd.models import XtdComment
from django_teams.models import Ownership
from project_share.models import Approval, Project


@receiver(post_save, sender=Approval)
def approval_handler(sender, instance, created, **kwargs):
    """When approval has an approver set project to approved."""
    if instance.approved_by is not None:
        instance.project.approved is True
        instance.project.save()


@receiver(post_save, sender=XtdComment)
def approval_comment(sender, instance, created, **kwargs):
    """If commended on comment is private until project is public."""
    if created is True:
        instance.is_public = False
        instance.save()


@receiver(post_save, sender=Ownership)  # noqa: F811
def approval_comment(sender, instance, created, **kwargs):
    """If approval is changed, set project to approved."""
    if instance.content_type == ContentType.objects.get(app_label="project_share", model="project") and\
       instance.approved is True:
        project = Project.objects.get(pk=instance.object_id)
        project.approved = True
        project.save()
