from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Game, Round
# Create your views here.

@login_required(login_url='/user/login')
def index(request):
    poker_active = "active"
    gameList = Game.objects.filter(owner=request.user)
    return render(request, "poker/index.html", locals())

@login_required(login_url='/user/login')
def detail(request, id):
    poker_active = "active"
    try:
        game = Game.objects.get(pk=id)
        if(game.owner != request.user):
            return redirect(reverse('poker_index'))
    except:
        return redirect(reverse('poker_index'))
    round_list = Round.objects.filter(game=game).order_by('-pk')
    sum1 = sum2 = sum3 = sum4 = 0
    for round in round_list:
        sum1 += round.score1
        sum2 += round.score2
        sum3 += round.score3
        sum4 += round.score4
    return render(request, "poker/detail.html", locals())

@login_required(login_url='/user/login')
def createGame(request):
    poker_active = "active"
    if request.method == 'POST':
        player1 = request.POST.get('player1', '')
        player2 = request.POST.get('player2', '')
        player3 = request.POST.get('player3', '')
        player4 = request.POST.get('player4', '')
        if(player1 and player2 and player3 and player4):
            game = Game.objects.create(owner=request.user, player1=player1, player2=player2, player3=player3, player4=player4)
            game.save()
            return redirect(reverse('poker_index'))
        else:
            message = "請輸入所有的欄位"
    return render(request, "poker/createGame.html", locals())

@login_required(login_url='/user/login')
def createRound(request, game_id):
    poker_active = "active"
    game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        score1 = int(request.POST.get('score1', 0))
        score2 = int(request.POST.get('score2', 0))
        score3 = int(request.POST.get('score3', 0))
        score4 = int(request.POST.get('score4', 0))
        sum = score1 + score2 + score3 + score4
        if(score1 == 0 or score1 == ''): score1 = sum
        else: score1 = -score1
        if(score2 == 0 or score2 == ''): score2 = sum
        else: score2 = -score2
        if(score3 == 0 or score3 == ''): score3 = sum
        else: score3 = -score3
        if(score4 == 0 or score4 == ''): score4 = sum
        else: score4 = -score4
        
        round = Round.objects.create(game=game, score1=score1, score2=score2, score3=score3, score4=score4)
        return redirect(reverse('poker_detail', args=(game_id,)))
    return render(request, "poker/createRound.html", locals())

@login_required(login_url='/user/login')
def apiEndGame(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.end_time = timezone.now()
    game.status = 1
    game.save()
    return redirect(reverse('poker_detail', args=(game_id,)))
