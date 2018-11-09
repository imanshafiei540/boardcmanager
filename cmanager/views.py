from django.shortcuts import render
from cmanager.models import *
import datetime

def addgame(request):
    if request.method == "POST":
        card_number = request.POST['card']
        user_select = User.objects.get(card_number=card_number)
        current_game = Game.objects.filter(user=user_select, end_time="00:00:00")
        if len(current_game):
            print(datetime.datetime.now().time())
            current_game[0].end_time = datetime.datetime.now().time()
            current_game[0].save()
        else:
            new_game = Game(user=user_select, start_time=datetime.datetime.now().time())
            new_game.save()

    return render(request, 'addgame.html')