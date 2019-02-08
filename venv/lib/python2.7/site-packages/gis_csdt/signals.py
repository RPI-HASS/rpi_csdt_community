from django.dispatch import receiver
from django.db.models.signals import post_save
from gis_csdt.models import Tag, TagIndiv


# @receiver(post_save, sender=Dataset)
def update_mappoints(sender, **kwargs):
    dataset = kwargs.get('instance')
    dataset.update_mappoints()
    # post_save.connect(update_mappoints, sender=Dataset)


@receiver(post_save, sender=TagIndiv)
def update_tag_count(sender, **kwargs):
    if kwargs.get('created'):  # if this is a new TagIndiv
        # increment the count and save
        kwargs.get('instance').tag.increment_count(save=True)


@receiver(post_save, sender=Tag)
def clean_tags(sender, **kwargs):
    # all tags must be lowercase without leading or trailing whitespace
    kwargs.get('instance').tag = kwargs.get('instance').tag.strip().lower()
