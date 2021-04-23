from django.urls import path
from .views import HomePageView, SearchResultsView, ReleaseDetailsView, add_release, delete_release, SearchArtistsView, \
    ArtistsView, ArtistDetailsView, add_artist, delete_artist, GenresView, SearchGenresView, add_genre, delete_genre, \
    GenreDetailsView, ChartsView, SearchChartsView, ChartDetailsView, add_chart_entry, CountriesView, LabelsView, \
    LabelDetailsView, SearchLabelsView, add_label_entry, SearchAllView, CountryDetailsView

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('search_all/', SearchAllView.as_view(), name='search_all'),
    path('search_artists/', SearchArtistsView.as_view(), name='search_artists'),
    path('search_genres/', SearchGenresView.as_view(), name='search_genres'),
    path('search_charts/', SearchChartsView.as_view(), name='search_charts'),
    path('search_labels/', SearchLabelsView.as_view(), name='search_labels'),
    path('', HomePageView.as_view(), name='home'),
    path('artists/', ArtistsView.as_view(), name='artists'),
    path('genres/', GenresView.as_view(), name='genres'),
    path('charts/', ChartsView.as_view(), name='charts'),
    path('countries/', CountriesView.as_view(), name='countries'),
    path('labels/', LabelsView.as_view(), name='labels'),
    path('releases/<int:pk>/', ReleaseDetailsView.as_view(), name='release_details'),
    path('artists/<int:pk>/', ArtistDetailsView.as_view(), name='artist_details'),
    path('genres/<int:pk>/', GenreDetailsView.as_view(), name='genre_details'),
    path('charts/<chart>/', ChartDetailsView.as_view(), name='chart_details'),
    path('countries/<int:pk>/', CountryDetailsView.as_view(), name='country_details'),
    path('labels/<label>/', LabelDetailsView.as_view(), name='label_details'),
    path('delete_release/<int:pk>/', delete_release, name='delete_release'),
    path('delete_artist/<int:pk>/', delete_artist, name='delete_artist'),
    path('delete_genre/<int:pk>/', delete_genre, name='delete_genre'),
    path('add_release/', add_release, name='add_release'),
    path('add_artist/', add_artist, name='add_artist'),
    path('add_genre/', add_genre, name='add_genre'),
    path('add_chart_entry/<int:pk>/', add_chart_entry, name='add_chart_entry'),
    path('add_label_entry/<int:pk>/', add_label_entry, name='add_label_entry'),
]
