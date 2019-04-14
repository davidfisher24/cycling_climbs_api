class PeakFilter(filters.FilterSet):
    from_date = filters.DateFilter(name="date", lookup_expr='gte')
    to_date = filters.DateFilter(name="date", lookup_expr='lte')

    class Meta:
      model = Track
      fields = ['date']