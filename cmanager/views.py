from django.shortcuts import render
from cmanager.models import *
import datetime


def addgame(request):
    if request.method == "POST":
        try:
            if request.POST['addorstop']:
                card_number = request.POST['card']
                nums = request.POST['numbers']
                user_select = User.objects.get(card_number=card_number)
                current_game = Game.objects.filter(user=user_select, end_time="00:00:00")
                if len(current_game):
                    current_game[0].end_time = datetime.datetime.now().time()
                    current_game[0].save()
                else:
                    new_game = Game(user=user_select, start_time=datetime.datetime.now().time(), numbers=nums)
                    new_game.save()
        except Exception as e:
            print(e)
            try:
                if request.POST['adduser'] == "true":
                    f_name = request.POST['fname']
                    l_name = request.POST['lname']
                    phone = request.POST['phone']
                    year = request.POST['year']
                    month = request.POST['month']
                    day = request.POST['day']
                    card = request.POST['card']
                    new_user = User(fisrt_name=f_name, last_name=l_name, phone=phone, year_of_birth=year, month_of_birth=month, day_of_birth=day, card_number=card)
                    new_user.save()
            except Exception as e:
                print(e)
                print("Nothing!")
    today_users = Game.objects.filter(add_date=datetime.datetime.now().date())
    users_list = []
    for e in today_users:
        start = e.start_time
        end = e.end_time
        timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
        timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
        t = timedelta_end - timedelta_start
        point = int(t.total_seconds() / 225)
        users_list.append({'user_obj': e, "price": point * 500, 'point': point})

    return render(request, 'addgame.html', {"user_data": users_list})