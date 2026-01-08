from datetime import timedelta

from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models.enums import IntegerChoices
from django.utils.timezone import now
from django_filters import FilterSet, NumberFilter, ChoiceFilter

from apps.models import User, Order


class UserFilterSet(FilterSet):
    # min_balance = NumberFilter(field_name="balance", lookup_expr='gte')  # gte - >=
    # max_balance = NumberFilter(field_name="balance", lookup_expr='lte')
    # is_owner = BooleanFilter(field_name="is_superuser", lookup_expr='exact')
    # # login_date = DateFilter(method="last_login_filter")
    # year = NumberFilter(method="last_login_year_filter")
    # turi = ChoiceFilter(field_name="type")
    number = NumberFilter(method='number_order_filter', label="buyurtmalar soni ..dan ko'plari")

    class Meta:
        model = User
        fields = []

    def number_order_filter(self, queryset, name, value):
        return queryset.annotate(count=Count('orders', filter=Q(orders__status=Order.Status.DELIVERED))).filter(
            count__gt=value)
    #
    # def last_login_year_filter(self, queryset, field_name, value):
    #     return queryset.filter(last_login__year=value)

    # def last_login_filter(self, queryset, field_name, value):
    #     return queryset.filter(last_login__date=value)


class OrderFilterSet(FilterSet):
    class PeriodChoice(IntegerChoices):
        ONE_DAY = 1, '1 Kun'
        THREE_DAY = 3, '3 Kun'
        ONE_WEEK = 7, '1 Hafta'

    period = ChoiceFilter(choices=PeriodChoice.choices, method='period_filter')

    class Meta:
        model = Order
        fields = []

    def period_filter(self, queryset, name, value):
        return queryset.filter(created_at__date__gte=now() - timedelta(days=int(value)))
