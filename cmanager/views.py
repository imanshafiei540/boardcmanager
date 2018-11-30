from django.shortcuts import render
from cmanager.models import *
import datetime


def addgame(request):
    users_list = []
    is_done_addorstop = 0
    is_done_adduser = 0
    if request.method == "POST":
        try:
            if request.POST['addorstop']:
                card_number = request.POST['card']
                card_number = card_number.replace("؟", "")
                card_number = card_number.replace("?", "")
                card_number = card_number.replace("%", "")
                nums = request.POST['numbers']
                user_select = User.objects.get(card_number=card_number)
                current_game = Game.objects.filter(user=user_select, end_time="00:00:00")
                if len(current_game):
                    current_game[0].end_time = datetime.datetime.now().time()
                    current_game[0].save()
                else:
                    new_game = Game(user=user_select, start_time=datetime.datetime.now().time(), numbers=nums,
                                    add_date=datetime.datetime.now().date())
                    new_game.save()
                is_done_addorstop = 1
        except Exception as e:
            print(e)
            try:
                if request.POST['adduser'] == "true":
                    f_name = request.POST['fname']
                    l_name = request.POST['lname']
                    phone = request.POST['phone']
                    intro = request.POST['intro']
                    year = request.POST['year']
                    month = request.POST['month']
                    day = request.POST['day']
                    card = request.POST['card']
                    card = card.replace("؟", "")
                    card = card.replace("?", "")
                    card = card.replace("%", "")
                    new_user = User(fisrt_name=f_name, last_name=l_name, phone=phone, year_of_birth=year,
                                    month_of_birth=month, day_of_birth=day, card_number=card, intro=intro)
                    new_user.save()
                    is_done_adduser = 1
            except Exception as e:
                print(e)
                print("Nothing!")
    today_users = Game.objects.filter(add_date=datetime.datetime.now().date()).order_by('-end_time')
    for e in today_users:
        point = 0
        start = e.start_time
        end = e.end_time
        timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
        if str(end) != "00:00:00":
            timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
            t = timedelta_end - timedelta_start
            point = int(round(t.total_seconds() / 225))
            users_list.append({'user_obj': e, "price": point * 500 * e.numbers, 'point': point * e.numbers, "end": 1})

    today_users_not_end = Game.objects.filter(add_date=datetime.datetime.now().date()).order_by('-start_time')
    for e in today_users_not_end:
        point = 0
        end = e.end_time
        if str(end) == "00:00:00":
            users_list.append({'user_obj': e, "price": point * 500 * e.numbers, 'point': point * e.numbers, "end": 0})

    return render(request, 'addgame.html',
                  {"user_data": users_list, "is_done_addorstop": is_done_addorstop, "is_done_adduser": is_done_adduser})


def refine_users(request):
    all_users = User.objects.all()
    for user in all_users:
        cnum = user.card_number
        cnum = cnum.replace("?", "")
        cnum = cnum.replace("%", "")
        cnum = cnum.replace("؟", "")
        user.card_number = cnum
        user.save()
