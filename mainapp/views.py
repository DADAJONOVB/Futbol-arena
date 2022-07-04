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
        first_club = int(request.POST.get('first_club'))
        second_club = int(request.POST.get('second_club'))
        r = Match.objects.get(id=match)
        r.first_club_result = first_club
        r.second_club_result = second_club
        r.status = False
        r.save()
        fc1 = Club.objects.get(id=r.first_club.id)
        fc2 = Club.objects.get(id=r.second_club.id)
        if first_club > second_club:
            fc1.point += 3
            fc1.win += 1
            fc1.scored += first_club
            fc1.missed += second_club
            fc1.total_goal += (first_club-second_club)
            fc2.lose += 1
            fc2.missed += first_club
            fc2.scored += second_club
            fc2.game += 1
            fc1.game += 1
            fc2.total_goal += (second_club - first_club)
            fc2.save()
            fc1.save()
        if first_club < second_club:
            fc2.point += 3
            fc2.win += 1
            fc2.scored += second_club
            fc2.missed += first_club
            fc2.game += 1
            fc1.game += 1
            fc2.total_goal += (second_club-first_club)
            fc1.lose += 1
            fc1.scored += first_club
            fc1.missed += second_club
            fc1.total_goal += (first_club-second_club)
            fc1.save()
            fc2.save()
        if first_club == second_club:
            fc1.point += 1
            fc2.point += 1
            fc1.scored += first_club
            fc1.missed += second_club
            fc1.total_goal += (first_club - second_club)
            fc2.scored += second_club
            fc2.missed += first_club
            fc2.total_goal += (second_club - second_club)
            fc2.game += 1
            fc1.game += 1
            fc1.draw += 1
            fc2.draw += 1
            fc1.save()
            fc2.save()
    return redirect("matches_url", round)


def UpdateMatch(request):
    if request.method == "POST":
        # start take data
        match = request.POST.get('match')
        first_club_result = int(request.POST.get('first_club_result'))
        second_club_result = int(request.POST.get('second_club_result'))
        # take obj from db
        match = Match.objects.get(id=match)
        f1 = Club.objects.get(id=match.first_club.id)
        f2 = Club.objects.get(id=match.second_club.id)
        round = match.round
        # chek results
        if match.first_club_result > match.second_club_result:
            result = 1
        elif match.second_club_result > match.first_club_result:
            result = 2
        else:
            result = 3
        #  update objects
        if result == 1:
            f1.scored -= match.first_club_result
            f2.scored -= match.second_club_result
            f1.missed -= match.second_club_result
            f2.missed -= match.first_club_result
            f1.game -= 1
            f2.game -= 1
            f1.point -= 3
            f1.win -= 1
            f2.lose -= 1
            f1.total_goal -= match.first_club_result - match.second_club_result
            f2.total_goal -= match.second_club_result - match.first_club_result
            f1.save()
            f2.save()
        if result == 2:
            f1.scored -= match.first_club_result
            f2.scored -= match.second_club_result
            f1.missed -= match.second_club_result
            f2.missed -= match.first_club_result
            f2.point -= 3
            f2.win -= 1
            f1.lose -= 1
            f1.game -= 1
            f2.game -= 1
            f1.total_goal -= match.first_club_result - match.second_club_result
            f2.total_goal -= match.second_club_result - match.first_club_result
            f1.save()
            f2.save()
        if result == 3:
            f1.scored -= match.first_club_result
            f2.scored -= match.second_club_result
            f1.missed -= match.second_club_result
            f2.missed -= match.first_club_result
            f1.point -= 1
            f2.point -= 1
            f1.game -= 1
            f2.game -= 1
            f1.draw -= 1
            f2.draw -= 1
            f1.total_goal += match.first_club_result - match.second_club_result
            f2.total_goal += match.second_club_result - match.first_club_result
            f1.save()
            f2.save()

        if first_club_result > second_club_result:
            f1.point += 3
            f1.win += 1
            f1.scored += first_club_result
            f1.missed += second_club_result
            f1.total_goal += (first_club_result-second_club_result)
            f2.lose += 1
            f2.missed += first_club_result
            f2.scored += second_club_result
            f2.game += 1
            f1.game += 1
            f2.total_goal += (second_club_result - first_club_result)
            f2.save()
            f1.save()
        if first_club_result < second_club_result:
            f2.point += 3
            f2.win += 1
            f2.scored += second_club_result
            f2.missed += first_club_result
            f2.game += 1
            f1.game += 1
            f2.total_goal += (second_club_result-first_club_result)
            f1.lose += 1
            f1.scored += first_club_result
            f1.missed += second_club_result
            f1.total_goal += (first_club_result-second_club_result)
            f1.save()
            f2.save()
        if first_club_result == second_club_result:
            f1.point += 1
            f2.point += 1
            f1.scored += first_club_result
            f1.missed += second_club_result
            f1.total_goal += (first_club_result - second_club_result)
            f2.scored += second_club_result
            f2.missed += first_club_result
            f2.total_goal += (second_club_result - first_club_result)
            f2.game += 1
            f1.game += 1
            f1.draw += 1
            f2.draw += 1
            f1.save()
            f2.save()
        match.first_club_result = first_club_result
        match.second_club_result = second_club_result
        match.save()
        return redirect('matches_url', round.id)


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
    clubs = Tournament.objects.get(id=pk).clubs.all().order_by("-point", '-total_goal', 'name')
    context = {
        'turs': turs,
        "tour": pk,
        'clubs': clubs
    }
    return render(request, 'turs.html', context)

import json

@login_required(login_url='login')
def turnir_matches_view(request, pk):
    matches = Match.objects.filter(round__pk=pk)
    tur = Round.objects.get(pk=pk)
    club = Club.objects.all()

    maxsulotjs = json.dumps(list(tur.tournament.clubs.values(
        'id', 'name'
    )))
    context = {
        'matches': matches,
        'tur': tur,
        'round': pk,
        'clubs': club,
        'maxsulotjs': maxsulotjs
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
        Match.objects.create(round_id=round, first_club_id=first_club, second_club_id=second_club)
    return redirect("matches_url", round)


def DeleteTournament(request, pk):
    Tournament.objects.get(id=pk).delete()
    return redirect('turnir_url')


def ChangeTournament(request, pk):
    if request.method == "POST":
        t = Tournament.objects.get(id=pk)
        name = request.POST.get("name")
        t.name = name
        if request.POST.get("date"):
            date = request.POST.get("date")
            t.data_start = date
        a = t.clubs.all()
        for i in a:
            t.clubs.remove(i)
        clubs = request.POST.getlist('clubs')
        for i in clubs:
            t.clubs.add(Club.objects.get(id=i))
        t.save()
    return redirect('turnir_url')


def ClubsView(request):
    club = list(Club.objects.all())
    dt = []
    for c in club:
        for t in Tournament.objects.all():
            if c in t.clubs.all():
                d = {
                    'id': c.id,
                    "status": "Active",
                    "tournament":  t.name,
                    "name": c.name,
                    "img": c.img,
                    'date': c.date,
                }
            else:
                d = {
                    'id': c.id,
                    "status": "Passive",
                    "tournament": "Turnirda qatnashmayapti",
                    "name": c.name,
                    "img": c.img,
                    'date': c.date,
                }
            dt.append(d)
    context = {
        "club": dt,
    }
    return render(request, 'clubs.html', context)


def AddClub(request):
    if request.method == "POST":
        name = request.POST.get("name")
        img = request.FILES.get("img")
        Club.objects.create(name=name, img=img)
    return redirect("clubs")

def DeleteMatch(request, pk):
    if request.method == "POST":
        round = request.POST.get("round")
        match = Match.objects.get(id=pk)
        f1 = Club.objects.get(id=match.first_club.id)
        f2 = Club.objects.get(id=match.second_club.id)
        round = match.round
        # chek results
        if match.first_club_result > match.second_club_result:
            result = 1
        elif match.second_club_result > match.first_club_result:
            result = 2
        else:
            result = 3
        #  update objects
        if result == 1:
            f1.scored -= match.first_club_result
            f2.scored -= match.second_club_result
            f1.missed -= match.second_club_result
            f2.missed -= match.first_club_result
            f1.game -= 1
            f2.game -= 1
            f1.point -= 3
            f1.win -= 1
            f2.lose -= 1
            f1.total_goal -= match.first_club_result - match.second_club_result
            f2.total_goal -= match.second_club_result - match.first_club_result
            f1.save()
            f2.save()
        if result == 2:
            f1.scored -= match.first_club_result
            f2.scored -= match.second_club_result
            f1.missed -= match.second_club_result
            f2.missed -= match.first_club_result
            f2.point -= 3
            f2.win -= 1
            f1.lose -= 1
            f1.game -= 1
            f2.game -= 1
            f1.total_goal -= match.first_club_result - match.second_club_result
            f2.total_goal -= match.second_club_result - match.first_club_result
            f1.save()
            f2.save()
        if result == 3:
            f1.scored -= match.first_club_result
            f2.scored -= match.second_club_result
            f1.missed -= match.second_club_result
            f2.missed -= match.first_club_result
            f1.point -= 1
            f2.point -= 1
            f1.game -= 1
            f2.game -= 1
            f1.draw -= 1
            f2.draw -= 1
            f1.total_goal += match.first_club_result - match.second_club_result
            f2.total_goal += match.second_club_result - match.first_club_result
            f1.save()
            f2.save()
        match.delete()
        return redirect("matches_url", round.id)
