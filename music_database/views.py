from django.contrib.postgres.search import SearchVector
from .models import Release, Artist, Genre, Chart, ChartsHaveReleases, Country, Label, LabelsHaveArtists
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .forms import ReleaseForm, ArtistForm, GenreForm, ChartsHaveReleasesForm, LabelsHaveArtistsForm
from django.http import HttpResponseRedirect
from accounts.models import User
from django.db.models import Q


class HomePageView(ListView):
    model = Release
    template_name = 'music_database_index.html'

    def get_queryset(self):
        return Release.objects.all().order_by('-id')[:12]


class ArtistsView(ListView):
    model = Artist
    template_name = 'artists.html'

    def get_queryset(self):
        return Artist.objects.all()


class GenresView(ListView):
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


class SearchGenresView(ListView):
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
        context['user'] = User.objects.get(username=self.request.user)
        context['artists'] = Release.objects.get(pk=self.kwargs['pk']).artists.all()
        context['genres'] = Release.objects.get(pk=self.kwargs['pk']).genres.all()
        return context


class ArtistDetailsView(DetailView):
    model = Artist
    template_name = 'artist_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user)
        context['releases'] = Artist.objects.get(pk=self.kwargs['pk']).release_set.all()
        return context


class GenreDetailsView(DetailView):
    model = Genre
    template_name = 'genre_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user)
        releases = Genre.objects.get(pk=self.kwargs['pk']).release_set.all()
        context['releases'] = releases
        return context


class ChartDetailsView(DetailView):
    model = ChartsHaveReleases
    template_name = 'chart_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = ChartsHaveReleases.objects.filter(chart_id=self.kwargs['pk'])
        context['chart'] = Chart.objects.get(pk=self.kwargs['pk'])
        return context


class LabelDetailsView(DetailView):
    model = LabelsHaveArtists
    template_name = 'label_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = LabelsHaveArtists.objects.filter(label_id=self.kwargs['pk'])
        context['label'] = Label.objects.get(pk=self.kwargs['pk'])
        return context


class SearchResultsView(ListView):
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
    model = Artist
    template_name = 'artists.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        country = self.request.GET.get('country')
        query_result = Artist.objects.filter(name__icontains=name)
        if country is not None:
            query_result = query_result & Artist.objects.filter(countries__name__icontains=country)
        return query_result


def add_release(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ReleaseForm(request.POST)
        if form.is_valid():
            added_object = form.save()
            added_object.entry_owner = user
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
