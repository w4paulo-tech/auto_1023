from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('autoservice.urls')),
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='autoservice/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
     static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
