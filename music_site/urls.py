from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('', include('music_database.urls')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
