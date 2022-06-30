from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def Home(request):
    return render(request, 'front/index.html')


def Loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.count() > 0:
            usr = authenticate(username=username, password=password)
            if usr is not None:
                login(request, usr)
                return redirect('dashboard_url')
            else:
                messages.error(request, 'Login yoki parol xato!')
                return redirect('login')
            return redirect('login')
        else:
            messages.error(request, 'Bunday foydalanuvchi mavjud emas!')
            return redirect('login')
    return render(request, 'auth-login.html')


def LogoutView(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def CloseMatch(request):
    if request.method == "POST":
        round = request.POST.get('round')
        match = request.POST.get('match')
        first_club = request.POST.get('first_club')
        second_club = request.POST.get('second_club')
        r = Match.objects.get(id=match)
        r.first_club_result = first_club
        r.second_club_result = second_club
        r.save()
    return redirect("matches_url", round)


@login_required(login_url='login')
def index_view(request):
    turnirs = Tournament.objects.all()[:3]
    context = {
        'turnirs': turnirs
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def turnir_view(request):
    turnirs = Tournament.objects.all()
    club = Club.objects.all()
    context = {
        'turnirs': turnirs,
        "clubs": club
    }
    return render(request, 'turnir.html', context)


@login_required(login_url='login')
def turnir_tur_view(request, pk):
    turs = Round.objects.filter(tournament__pk=pk)
    clubs = Tournament.objects.get(id=pk).clubs.all().order_by("-point", '-total_goal')
    context = {
        'turs': turs,
        "tour": pk,
        'clubs': clubs
    }
    return render(request, 'turs.html', context)


@login_required(login_url='login')
def turnir_matches_view(request, pk):
    matches = Match.objects.filter(round__pk=pk)
    tur = Round.objects.get(pk=pk)
    club = Club.objects.all()
    context = {
        'matches': matches,
        'tur': tur,
        'round': pk,
        'clubs': club,
    }
    return render(request, 'matches.html', context)


@login_required(login_url='login')
def AddTournament(request):
    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')
        club = request.POST.getlist('clubs')
        t = Tournament.objects.create(name=name, data_start=date)
        for i in club:
            t.clubs.add(Club.objects.get(id=i))
    return redirect('turnir_url')


@login_required(login_url='login')
def AddRound(request):
    if request.method == "POST":
        tournament = request.POST.get("tournament")
        name = request.POST.get('name')
        date = request.POST.get('date')
        Round.objects.create(tournament_id=tournament, name=name, data_start=date)
    return redirect("tur_url", tournament)


@login_required(login_url='login')
def AddMatch(request):
    if request.method == "POST":
        round = request.POST.get("round")
        first_club = request.POST.get("first_club")
        second_club = request.POST.get("second_club")
        print(first_club, second_club)
        Match.objects.create(round_id=round, first_club_id=first_club, second_club_id=second_club)
    return redirect("matches_url", round)

