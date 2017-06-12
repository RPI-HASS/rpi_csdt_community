from django.contrib import admin

# Register your models here.
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    exclude = ('height_field', 'width_field')
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["title", "content"]

    class Meta:
        model = Post
        exclude = ('height_field', 'width_field')


admin.site.register(Post, PostModelAdmin)
