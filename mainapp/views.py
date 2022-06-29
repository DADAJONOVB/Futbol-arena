from django.shortcuts import render
from .models import *


def index_view(request):
    turnirs = Tournament.objects.all()[:3]
    context = {
        'turnirs': turnirs
    }
    return render(request, 'index.html', context)


def turnir_view(request):
    turnirs = Tournament.objects.all()
    context = {
        'turnirs': turnirs
    }
    return render(request, 'turnir.html', context)


def turnir_tur_view(request, pk):
    turs = Round.objects.filter(tournament__pk=pk)
    context = {
        'turs': turs
    }
    return render(request, 'turs.html', context)


def turnir_matches_view(request, pk):
    matches = Match.objects.filter(round__pk=pk)
    tur = Round.objects.get(pk=pk)
    context = {
        'matches': matches,
        'tur': tur
    }
    return render(request, 'matches.html', context)

