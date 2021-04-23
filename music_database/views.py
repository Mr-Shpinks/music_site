from django.contrib.postgres.search import SearchVector
from .models import Release, Artist, Genre, Chart, ChartsHaveReleases, Country, Label, LabelsHaveArtists, Country
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .forms import ReleaseForm, ArtistForm, GenreForm, ChartsHaveReleasesForm, LabelsHaveArtistsForm
from django.http import HttpResponseRedirect
from accounts.models import User
from django.db.models import Q
from django.core.paginator import Paginator
import itertools
from django.shortcuts import get_object_or_404


class HomePageView(ListView):
    paginate_by = 12
    model = Release
    template_name = 'music_database_index.html'

    def get_queryset(self):
        return Release.objects.all().order_by('-id')


class ArtistsView(ListView):
    paginate_by = 50
    model = Artist
    template_name = 'artists.html'

    def get_queryset(self):
        return Artist.objects.all()


class GenresView(ListView):
    paginate_by = 50
    model = Genre
    template_name = 'genres.html'

    def get_queryset(self):
        return Genre.objects.all()


class ChartsView(ListView):
    model = Chart
    template_name = 'charts.html'

    def get_queryset(self):
        return Chart.objects.all()


class CountriesView(ListView):
    model = Country
    template_name = 'countries.html'

    def get_queryset(self):
        return Country.objects.all()


class LabelsView(ListView):
    model = Label
    template_name = 'labels.html'

    def get_queryset(self):
        return Label.objects.all()


class SearchAllView(ListView):
    paginate_by = 50
    template_name = 'all_search_results.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        releases = Release.objects.filter(name__icontains=name)
        artists = Artist.objects.filter(name__icontains=name)
        genres = Genre.objects.filter(name__icontains=name)
        charts = Chart.objects.filter(name__icontains=name)
        countries = Country.objects.filter(name__icontains=name)
        labels = Label.objects.filter(name__icontains=name)
        query_result = list(itertools.zip_longest(releases, artists, genres, charts, countries, labels))
        return query_result


class SearchGenresView(ListView):
    paginate_by = 50
    model = Genre
    template_name = 'genres.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        query_result = Genre.objects.filter(name__icontains=name)
        return query_result


class SearchChartsView(ListView):
    model = Chart
    template_name = 'charts.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        query_result = Chart.objects.filter(name__icontains=name)
        return query_result


class SearchLabelsView(ListView):
    model = Label
    template_name = 'labels.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        query_result = Label.objects.filter(name__icontains=name)
        return query_result


class ReleaseDetailsView(DetailView):
    model = Release
    template_name = 'release_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user'] = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            context['user'] = None
        context['artists'] = Release.objects.get(pk=self.kwargs['pk']).artists.all()
        context['genres'] = Release.objects.get(pk=self.kwargs['pk']).genres.all()
        return context


class ArtistDetailsView(DetailView):
    model = Artist
    template_name = 'artist_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['user'] = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            context['user'] = None

        context['releases'] = Artist.objects.get(pk=self.kwargs['pk']).release_set.all()
        return context


class GenreDetailsView(DetailView):
    model = Genre
    template_name = 'genre_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user'] = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            context['user'] = None
        releases = Genre.objects.get(pk=self.kwargs['pk']).release_set.all()
        context['releases'] = releases
        return context


class ChartDetailsView(ListView):
    paginate_by = 50
    template_name = 'chart_details.html'

    def get_queryset(self):
        self.chart = get_object_or_404(Chart, pk=self.kwargs['chart'])
        query_set = ChartsHaveReleases.objects.filter(chart_id=self.chart)
        release_name = self.request.GET.get('release_name')
        pos_from = self.request.GET.get('pos_from')
        pos_to = self.request.GET.get('pos_to')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from is not None and date_from != '':
            query_set = query_set & ChartsHaveReleases.objects.filter(date__gte=date_from)

        if date_to is not None and date_to != '':
            query_set = query_set & ChartsHaveReleases.objects.filter(date__lte=date_to)

        if pos_from is not None and pos_from != '':
            query_set = query_set & ChartsHaveReleases.objects.filter(position__lte=pos_from)

        if pos_to is not None and pos_to != '':
            query_set = query_set & ChartsHaveReleases.objects.filter(position__gte=pos_to)

        if release_name is not None and release_name != '':
            query_set = query_set & ChartsHaveReleases.objects.filter(chart_id=self.chart).select_related(
                'release').filter(release__name__icontains=release_name)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user'] = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            context['user'] = None
        context['chart'] = self.chart
        return context


class CountryDetailsView(DetailView):
    model = Country
    template_name = 'country_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artists = Country.objects.get(pk=self.kwargs['pk']).artist_set.all()
        context['artists'] = artists
        return context


class LabelDetailsView(ListView):
    paginate_by = 50
    template_name = 'label_details.html'

    def get_queryset(self):
        self.label = get_object_or_404(Label, pk=self.kwargs['label'])
        query_set = LabelsHaveArtists.objects.filter(label_id=self.label)
        artist_name = self.request.GET.get('artist_name')

        if artist_name is not None and artist_name != '':
            query_set = query_set & LabelsHaveArtists.objects.filter(label_id=self.label).select_related(
                'artist').filter(artist__name__icontains=artist_name)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user'] = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            context['user'] = None
        context['label'] = self.label
        return context


class SearchResultsView(ListView):
    paginate_by = 18
    model = Release
    template_name = 'search_results.html'

    def get_queryset(self):
        name = self.request.GET.get('name') if self.request.GET.get('name') is not None else ''
        date = self.request.GET.get('date') if self.request.GET.get('date') is not None else ''
        artist = self.request.GET.get('artist') if self.request.GET.get('artist') is not None else ''
        genre = self.request.GET.get('genre') if self.request.GET.get('genre') is not None else ''
        # check name and date ilike
        query_result = Release.objects.filter(Q(name__icontains=name) & Q(date__icontains=date))
        # check artists names ilike if input is not empty
        if artist != '':
            query_result = query_result & Release.objects.filter(Q(artists__name__icontains=artist))
        # check genres names ilike if input is not empty
        if genre != '':
            query_result = query_result & Release.objects.filter(Q(genres__name__icontains=genre))
        return query_result


class SearchArtistsView(ListView):
    paginate_by = 50
    model = Artist
    template_name = 'artists.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        country = self.request.GET.get('country')
        query_result = Artist.objects.filter(name__icontains=name)
        if country is not None and country != '':
            query_result = query_result & Artist.objects.filter(countries__name__icontains=country)
        return query_result


def add_release(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ReleaseForm(request.POST)
        if form.is_valid():
            added_object = form.save()
            added_object.entry_owner = user
            added_object.cover = request.FILES['cover']
            added_object.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = ReleaseForm()
        return render(request, 'add_release.html', {'form': form})


def add_artist(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            added_object = form.save()
            added_object.entry_owner = user
            added_object.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = ArtistForm()
        return render(request, 'add_artist.html', {'form': form})


def add_genre(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            added_object = form.save()
            added_object.entry_owner = user
            added_object.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = GenreForm()
        return render(request, 'add_genre.html', {'form': form})


def add_chart_entry(request, pk):
    if request.method == 'POST':
        form = ChartsHaveReleasesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/charts/{pk}/')
    else:
        form = ChartsHaveReleasesForm(initial={'chart': Chart.objects.get(pk=pk)})
        return render(request, 'add_genre.html', {'form': form})  # add_genre works fine


def add_label_entry(request, pk):
    if request.method == 'POST':
        form = LabelsHaveArtistsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/labels/{pk}/')
    else:
        form = LabelsHaveArtistsForm(initial={'label': Label.objects.get(pk=pk)})
        return render(request, 'add_genre.html', {'form': form})  # add_genre works fine


def delete_release(request, pk):
    release = None
    try:
        release = Release.objects.get(pk=pk)
    except Release.DoesNotExist as e:
        print(e)

    if release is not None and request.user == release.entry_owner:
        release.delete()
    return HttpResponseRedirect('/')


def delete_artist(request, pk):
    artist = None
    try:
        artist = Artist.objects.get(pk=pk)
    except Artist.DoesNotExist as e:
        print(e)

    if artist is not None and request.user == artist.entry_owner:
        artist.delete()
    return HttpResponseRedirect('/artists/')


def delete_genre(request, pk):
    genre = None
    try:
        genre = Genre.objects.get(pk=pk)
    except Genre.DoesNotExist as e:
        print(e)

    if genre is not None and request.user == genre.entry_owner:
        genre.delete()
    return HttpResponseRedirect('/genres/')
