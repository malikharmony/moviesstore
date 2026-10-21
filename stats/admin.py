from django.contrib import admin
from .models import *
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Max, Sum
from django.template.response import TemplateResponse

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

@admin.register(MovieStat)
class MovieStatAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj =None):
        return False
    def has_delete_permission(self, request, obj =None):
        return False

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_permission(request):
            raise PermissionDenied

        purchases = MovieStat.objects.annotate(
            total=Sum('item__quantity')
        )

        reviews = MovieStat.objects.annotate(
            total=Count('review')
        )

        purchase_max = purchases.aggregate(
            highest=Max('total')
        )['highest']

        review_max = reviews.aggregate(
            highest=Max('total')
        )['highest']

        most_purchased = []

        if purchase_max and purchase_max > 0:
            most_purchased = purchases.filter(
                total=purchase_max
            ).order_by('name', 'pk')

        most_reviewed = []

        if review_max and review_max > 0:
            most_reviewed = reviews.filter(
                total=review_max
            ).order_by('name', 'pk')

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Movie statistics',
            'most_purchased': most_purchased,
            'most_reviewed': most_reviewed,
            **(extra_context or {})
        }

        return TemplateResponse(
            request,
            'admin/stats/movie_statistics.html',
            context,
        )
