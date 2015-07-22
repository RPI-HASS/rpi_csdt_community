from django.db.models.signals import post_save
from django.dispatch import receiver

from project_share.models import Approval, Project
from django_teams.models import Ownership
from django_comments_xtd.models import XtdComment

@receiver(post_save, sender=Approval)
def approval_handler(sender, instance, created, **kwargs):
    if instance.approved_by != None:
        instance.project.approved = True
        instance.project.save()

@receiver(post_save, sender=XtdComment)
def approval_comment(sender, instance, created, **kwargs):
    if created == True:
        instance.is_public = False
        instance.save()
		
@receiver(post_save, sender=Ownership)
def approval_comment(sender, instance, created, **kwargs):
    if instance.content_type == ContentType.objects.get(app_label="project_share", model="project") and instance.approved == True:
        p = Project.objects.get(pk=instance.object_id)
        p.approved = True
        p.save() 