from django.contrib import admin
from django.urls import path, include
from quotes import urls as quotes_urls
from core import urls as core_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include(quotes_urls, namespace='quotes')),
    path('', include(core_urls, namespace='core')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
