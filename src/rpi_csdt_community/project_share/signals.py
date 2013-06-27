from django.db.models.signals import post_save
from django.dispatch import receiver

from project_share.models import Approval

@receiver(post_save, sender=Approval)
def approval_handler(sender, instance, created, **kwargs):
    if instance.approved_by != None:
        instance.project.approved = True
        instance.project.save()
