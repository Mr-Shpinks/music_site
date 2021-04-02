from django.urls import path
from .views import HomePageView, SearchResultsView, ReleaseDetailsView

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', HomePageView.as_view(), name='home'),
    path('releases/<int:pk>/', ReleaseDetailsView.as_view(), name='release_details'),
]
