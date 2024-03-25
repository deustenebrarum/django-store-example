from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def profile_view(request: HttpRequest):
    return HttpResponse(render(request, 'profile.html', {}))
