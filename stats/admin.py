from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserStat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('name', 'purchaseTotal')
    ordering = ('-purchaseTotal',)
    change_list_template = 'admin/stats/change_list.html'

    def name(self, obj):
        return obj.user.username
    name.short_description = "Username"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if 'list_size' in request.GET:
            request.GET = request.GET.copy()
            list_size = request.GET.pop('list_size')[0]
            request.list_size = list_size
            extra_context['list_size'] = list_size
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request).order_by('-purchaseTotal')
        list_size = getattr(request, 'list_size', None)
        if list_size and list_size.isdigit():
            top_ids = list(qs.values_list('id', flat=True)[:int(list_size)])
            return qs.filter(id__in=top_ids)
        return qs
