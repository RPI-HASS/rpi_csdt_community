from django.shortcuts import render
from extra_views import SearchableListMixin, SortableListMixin
from django.views.generic import ListView

from .models import Entry
from project_share.models import Application

# Create your views here.


def filter_project_query(set, request):
    filter_val = request.GET.get('filter')
    if filter_val is not None:
        set = set.filter(application=filter_val,)
    term = request.GET.get('q')
    if term is not None:
        set = set.filter(Q(name__icontains=term) | Q(
            description__icontains=term))
    order = request.GET.get('orderby')
    if order is not None:
        set = set.order_by(order)
    else:
        set = set.order_by("-id")
    return set


class EntryListView(SearchableListMixin, SortableListMixin, ListView):
    """List all entries, but make sortable."""

    sort_fields_aliases = [('name', 'by_name'), ('id', 'by_id'), ]
    # search_fields = [('name', 'iexact')]
    search_split = False
    model = Entry
    paginate_by = 100
    ordering = ["-when"]

    def get_queryset(self):
        """Order projects based on filter or order request settings."""
        queryset = Entry.objects.all()
        return filter_project_query(queryset, self.request)

    def render_to_response(self, context, **response_kwargs):
        """List all applications for the user to choose to filter by."""
        application_list = Application.objects.all()
        context['application_list'] = application_list
        context['order'] = self.request.GET.get('orderby')
        filter_val = self.request.GET.get('filter')
        context['filter_val'] = filter_val
        if filter_val:
            context['name'] = application_list.get(id=filter_val)
        context['term'] = self.request.GET.get('q')
        return super(EntryListView, self).render_to_response(context, **response_kwargs)
