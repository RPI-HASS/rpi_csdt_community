from django.contrib import admin

# Register your models here.
from .models import Post, MyCustomTag
from taggit.admin import Tag

admin.site.unregister(Tag)


class PostModelAdmin(admin.ModelAdmin):
    exclude = ('height_field', 'width_field')
    list_display = ["title", "updated", "timestamp", 'tag_list']
    list_display_links = ["updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        return super(PostModelAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in Post.tags.all())

    class Meta:
        model = Post
        exclude = ('height_field', 'width_field')


class TaggitModelAdmin(admin.ModelAdmin):
    class Meta:
        model = MyCustomTag


admin.site.register(Post, PostModelAdmin)


admin.site.register(MyCustomTag, TaggitModelAdmin)
