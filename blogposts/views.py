try:
    from urllib import quote_plus  # python 2  # NOQA
except:
    from urllib.parse import quote_plus  # python 3  # NOQA
    pass

from comments.forms import CommentForm
from comments.models import Comment
import datetime
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from .forms import PostForm
from .models import Post


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


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


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by('-publish')
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    tags = Post.tags.most_common().order_by("rank")
    now = datetime.datetime.now()
    events = list(queryset_list)
    event_dict = []
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
                event_dict.append(year)
                year = []
                month = []
                month.append(event)
        year.append(month)
        event_dict.append(year)
    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
        "tags": tags,
        'now': now,
        'list_events': event_dict,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("blogposts:list")


class ViewTag(ListView):
    template_name = "blogposts/filter.html"

    def get_queryset(self):
        tag = self.kwargs['tag']
        queryset_list = Post.objects.filter(tags__name__in=[tag])
        paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
        page_request_var = "page"
        page = self.request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)
        return queryset

    def get_tag(self):
        tag = self.kwargs['tag']
        return tag

    def tag_calendar(self):
        tag = self.kwargs['tag']
        queryset_list = Post.objects.filter(tags__name__in=[tag])
        paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
        page_request_var = "page"
        page = self.request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)
        events = list(queryset)
        event_dict = []
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
                    event_dict.append(year)
                    year = []
                    month = []
                    month.append(event)
            year.append(month)
            event_dict.append(year)
        return event_dict

    def tags(self):
        return Post.tags.all()


class DateSearch(ListView):
    template_name = "blogposts/date.html"

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        return Post.objects.filter(publish__year=year, publish__month=month, publish__day=day)

    def get_tag(self):
        tag = self.kwargs['tag']
        return tag
