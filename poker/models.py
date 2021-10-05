from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Game(models.Model):
    STATUS = (
        (0, '進行中'),
        (1, '已結束'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="擁有者")
    player1 = models.CharField(max_length=10, verbose_name="玩家1")
    player2 = models.CharField(max_length=10, verbose_name="玩家2")
    player3 = models.CharField(max_length=10, verbose_name="玩家3")
    player4 = models.CharField(max_length=10, verbose_name="玩家4")
    status = models.IntegerField(choices=STATUS, default=0, verbose_name="遊戲狀態")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="開始時間")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="結束時間")

class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="對應場")
    score1 = models.IntegerField(verbose_name="玩家1分數")
    score2 = models.IntegerField(verbose_name="玩家2分數")
    score3 = models.IntegerField(verbose_name="玩家3分數")
    score4 = models.IntegerField(verbose_name="玩家4分數")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="記錄時間")
    


