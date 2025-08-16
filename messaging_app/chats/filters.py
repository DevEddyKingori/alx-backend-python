import django_filters
from .models import Message
from django.db.models import Q
from django.utils import timezone

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='iexact')
    start_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(content__icontains=value) |
            Q(sender__username__icontains=value)