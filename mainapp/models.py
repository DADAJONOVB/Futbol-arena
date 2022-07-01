from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='club/', null=True, blank=True)
    game = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    scored = models.IntegerField(default=0)
    missed = models.IntegerField(default=0)
    total_goal = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=255) 
    data_start = models.DateField()
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='one', null=True, blank=True)
    second_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='two', null=True, blank=True)
    third_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='three', null=True, blank=True)
    clubs = models.ManyToManyField(Club, related_name='clubs')

    def __str__(self):
        return self.name
    

class Round(models.Model):
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    data_start = models.DateField()

    def __str__(self):
        return self.name


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    first_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='first')
    second_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='second')
    first_club_result = models.PositiveIntegerField(default=0)
    second_club_result = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_club}, {self.second_club}"

