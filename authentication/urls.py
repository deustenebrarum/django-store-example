from django.urls import include, path

from .views import profile_view


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile_view, name='profile'),
]
