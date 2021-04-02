from django.contrib.postgres.search import SearchVector
from .models import Release
from django.views.generic import ListView, DetailView


class HomePageView(ListView):
    model = Release
    template_name = 'music_database_index.html'

    def get_queryset(self):
        return Release.objects.all().order_by('-id')[:12]


class ReleaseDetailsView(DetailView):
    model = Release
    template_name = 'release_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchResultsView(ListView):
    model = Release
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Release.objects.annotate(search=SearchVector('name', 'year')).filter(search=query)
