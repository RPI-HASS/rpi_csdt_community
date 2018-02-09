try:
    from urllib import quote_plus  # python 2  # NOQA
except:
    from urllib.parse import quote_plus  # python 3  # NOQA
    pass

from comments.forms import CommentForm
from comments.models import Comment
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from extra_views import SearchableListMixin, SortableListMixin
from django.views.generic import ListView
from .models import Post


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content.encode('utf8'))

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "post_detail.html", context)


def get_calendar(objects):
    events = list(objects)
    event_calendar = []
    year = []
    month = []
    if events:
        month.append(events[0])
        for i in range(1, len(events)):
            event = events[i]
            current = month[0]
            if current.publish.year == event.publish.year and current.publish.month == event.publish.month:
                month.append(event)
            elif current.publish.year == event.publish.year:
                year.append(month)
                month = []
                month.append(event)
            else:
                year.append(month)
                event_calendar.append(year)
                year = []
                month = []
                month.append(event)
        year.append(month)
        event_calendar.append(year)
    return event_calendar


class post_list(SearchableListMixin, SortableListMixin, ListView):
    model = Post
    template_name = "post_list.html"
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Post.objects.all().order_by('-publish')
        else:
            queryset = Post.objects.active().order_by('-publish')
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                                       Q(title__icontains=query) | # noqa E126
                                       Q(content__icontains=query) |
                                       Q(user__first_name__icontains=query) |
                                       Q(user__last_name__icontains=query) |
                                       Q(tags__name__icontains=query)).distinct()
        tags = self.request.GET.get('tag')
        if tags:
            queryset = queryset.filter(tags__name__in=[tags])
        return queryset

    def render_to_response(self, context, **response_kwargs):
        available_tags = Post.tags.most_common().order_by("rank")
        selected_tags = self.request.GET.get('tag')
        print(selected_tags)
        now = datetime.datetime.now()
        today = timezone.now().date()
        context['today'] = today
        context['available_tags'] = available_tags
        context['selected_tags'] = selected_tags
        context['now'] = now
        context['list_events'] = get_calendar(self.object_list)
        return super(post_list, self).render_to_response(context, **response_kwargs)
