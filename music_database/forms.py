from django.forms import ModelForm
from .models import Release, Artist, Genre, ChartsHaveReleases, LabelsHaveArtists
from django.contrib.admin.widgets import FilteredSelectMultiple


class ReleaseForm(ModelForm):
    class Meta:
        model = Release
        exclude = ['charts', 'entry_owner']


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'countries']


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class ChartsHaveReleasesForm(ModelForm):
    class Meta:
        model = ChartsHaveReleases
        fields = '__all__'


class LabelsHaveArtistsForm(ModelForm):
    class Meta:
        model = LabelsHaveArtists
        fields = '__all__'
