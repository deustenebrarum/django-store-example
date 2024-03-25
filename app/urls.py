from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from app.settings import MEDIA_ROOT, MEDIA_URL

from main.urls import urlpatterns as main_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_urls)),
    path('auth/', include('django.contrib.auth.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
