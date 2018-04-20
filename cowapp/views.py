from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    return HttpResponse('It is cowapp test page. Wow It\'s successful!!')
