from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Game, Round
# Create your views here.


@login_required(login_url='/user/login')
def index(request):
    poker_active = "active"
    game_name = "撲克"
    game_create_url = "poker_create_game"
    game_detail_url = "poker_detail"
    gameList = Game.objects.filter(owner=request.user)
    return render(request, "index.html", locals())

@login_required(login_url='/user/login')
def detail(request, id):
    poker_active = "active"
    game_name = "撲克"
    game_create_url = "poker_create_round"
    game_end_url = "poker_end_game"
    try:
        game = Game.objects.get(pk=id)
        if(game.owner != request.user):
            return redirect(reverse('poker_index'))
    except:
        return redirect(reverse('poker_index'))
    round_list = Round.objects.filter(game=game).order_by('-pk')
    sum1 = sum2 = sum3 = sum4 = 0
    win1 = win2 = win3 = win4 = 0
    for round in round_list:
        if(round.score1 > 0): win1 += 1
        if(round.score2 > 0): win2 += 1
        if(round.score3 > 0): win3 += 1
        if(round.score4 > 0): win4 += 1
        sum1 += round.score1
        sum2 += round.score2
        sum3 += round.score3
        sum4 += round.score4
    total_win = len(round_list)
    win1 /= float(total_win)
    win2 /= float(total_win)
    win3 /= float(total_win)
    win4 /= float(total_win)
    win1 *= 100
    win2 *= 100
    win3 *= 100
    win4 *= 100
    return render(request, "detail.html", locals())

@login_required(login_url='/user/login')
def createGame(request):
    poker_active = "active"
    game_name = "撲克"
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
    return render(request, "createGame.html", locals())

@login_required(login_url='/user/login')
def createRound(request, game_id):
    poker_active = "active"
    game_name = "撲克"
    game_detail_url = "poker_detail"
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
    return render(request, "createRound.html", locals())

@login_required(login_url='/user/login')
def apiEndGame(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.end_time = timezone.now()
    game.status = 1
    game.save()
    return redirect(reverse('poker_detail', args=(game_id,)))

@login_required(login_url='/user/login')
def apiGetRound(request, round_id):
    round = Round.objects.get(pk=round_id)
    html = '''
        %s: %d<br>
        %s: %d<br>
        %s: %d<br>
        %s: %d<br>
    ''' % (round.game.player1, round.score1,
           round.game.player2, round.score2,
           round.game.player3, round.score3,
           round.game.player4, round.score4)
    return HttpResponse(html)

@login_required(login_url='/user/login')
def apiDeleteRound(request, round_id):
    round = Round.objects.get(pk=round_id)
    game = round.game
    round.delete()
    return redirect('poker_detail', (game.id))
