from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    return HttpResponse('It is cowapp test page. Wow It\'s successful!! 2222222222 3333333333333333')
