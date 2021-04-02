from django.contrib import admin
from .models import Release, Artist, Genre, Label, Country, Chart, LabelsHaveArtists, ChartsHaveReleases


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "release_type", "origin", "issue", "status", "related")
    filter_horizontal = ("artists", "genres",)  # widget for searching


class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    filter_horizontal = ("countries",)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class LabelAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class ChartAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class LabelsHaveArtistsAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "artist", "date_from", "date_to")


class ChartsHaveReleasesAdmin(admin.ModelAdmin):
    list_display = ("id", "chart", "release", "position", "date")


admin.site.register(Release, ReleaseAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Chart, ChartAdmin)
admin.site.register(LabelsHaveArtists, LabelsHaveArtistsAdmin)
admin.site.register(ChartsHaveReleases, ChartsHaveReleasesAdmin)
