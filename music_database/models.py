from django.db import models
from enum import Enum
from django.db.models import Q, F
from django.db.models.functions import Now, Cast
from django.db.models.signals import post_delete
from django.dispatch import receiver
from accounts.models import User


class IterableEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Origin(IterableEnum):
    studio = 'studio'
    live = 'live'
    compilation = 'compilation'


class ReleaseType(IterableEnum):
    album = 'album'
    single = 'single'
    track = 'track'


class Issue(IterableEnum):
    original = 'original'
    reissue = 'reissue'
    remaster = 'remaster'


class Status(IterableEnum):
    released = 'released'
    upcoming = 'upcoming'


class Artist(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    labels = models.ManyToManyField('Label', blank=True, through='LabelsHaveArtists')
    countries = models.ManyToManyField('Country', blank=True)

    entry_owner = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    entry_owner = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Release(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateField(null=False)
    origin = models.CharField(max_length=15, choices=Origin.choices(), blank=True, null=True)
    release_type = models.CharField(max_length=15, choices=ReleaseType.choices(), blank=False, null=False)
    issue = models.CharField(max_length=15, choices=Issue.choices(), blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices(), blank=False, null=False)
    related = models.ForeignKey('Release', on_delete=models.CASCADE, blank=True, null=True)

    cover = models.ImageField(upload_to='album_covers/', blank=True, null=True)

    artists = models.ManyToManyField(Artist, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    charts = models.ManyToManyField('Chart', blank=True, through='ChartsHaveReleases')

    entry_owner = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        constraints = [
            # albums and singles cannot be included in other albums and singles
            models.CheckConstraint(
                check=~Q(release_type__in=('single', 'album')) | Q(related__exact=None),
                name='related_constrain'
            ),
            # upcoming releases can only be added with future dates
            models.CheckConstraint(
                # Now() for statement_timestamp() on database server
                check=Q(status__exact='upcoming') & Q(date__gt=Now()) |  # gt for greater than
                      Q(status__exact='released') & Q(date__lte=Now()),  # lte for less than or equal
                name='date_status'
            ),
            # track cannot be a compilation
            models.CheckConstraint(
                check=~Q(release_type__exact='track') | ~Q(origin__exact='compilation'),
                name='track_cannot_be_compilation'
            )
        ]

    @staticmethod
    def get_queryset():
        return Release.objects.all()

    def get_related_release_object(self):
        return Release.objects.get(pk=self.related.id) if self.related is not None else None

    def __str__(self):
        return self.name


# delete an actual image file on server after deletion of model instance from database
@receiver(post_delete, sender=Release)
def image_file_deletion(sender, instance, **kwargs):  # all signal handlers must take sender and **kwargs arguments.
    instance.cover.delete(False)


class Label(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    artists = models.ManyToManyField(Artist, blank=True, through='LabelsHaveArtists')

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = u'Countries'

    def __str__(self):
        return self.name


class Chart(models.Model):
    name = models.CharField(max_length=50)
    releases = models.ManyToManyField(Release, blank=True, through='ChartsHaveReleases')

    def __str__(self):
        return self.name


class ChartsHaveReleases(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, null=False)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=False)
    position = models.SmallIntegerField(null=False)
    date = models.DateField(null=False)

    class Meta:
        verbose_name_plural = u'Charts-releases relationships'
        unique_together = (('chart', 'release', 'date'),)
        constraints = [
            models.CheckConstraint(
                check=Q(date__lte=Now()),
                name='date_should_be_equal_or_less_than_current'
            ),
            models.CheckConstraint(
                check=Q(position__gte=1),
                name='position_1_or_greater'
            ),
        ]

    def get_release_object(self):
        return Release.objects.get(pk=self.release.id)


class LabelsHaveArtists(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, null=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=False)
    date_from = models.DateField(null=False)
    date_to = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = u'Labels-artists relationships'
        unique_together = (('label', 'artist', 'date_from'),)
        constraints = [
            models.CheckConstraint(
                check=Q(date_to__gte=F('date_from')),
                name='date_from_should_be_equal_or_less_than_date_to'
            )
        ]

    def get_artist_object(self):
        return Artist.objects.get(pk=self.artist.id)
