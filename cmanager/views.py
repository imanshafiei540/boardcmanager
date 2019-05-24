from django.shortcuts import render, redirect
from cmanager.models import *
import datetime
from cmanager.fusioncharts.fusioncharts import FusionCharts
import jdatetime


def addgame(request):
    users_list = []
    is_done_addorstop = 0
    is_done_adduser = 0
    is_done_addcredit = 0
    if request.method == "POST":
        try:
            if request.POST['addcredit'] == "true":
                credit = request.POST['credit']
                card_number = request.POST['card']
                card_number = card_number.replace("؟", "")
                card_number = card_number.replace("?", "")
                card_number = card_number.replace("%", "")
                user_select = User.objects.get(card_number=card_number)
                user_select.credit += int(credit)
                user_select.save()
                is_done_addcredit = 1
        except:
            pass

        try:
            if request.POST['addorstop']:
                card_number = request.POST['card']
                if 'used_credit' in request.POST:
                    used_credit = request.POST['used_credit']
                else:
                    used_credit = "off"
                card_number = card_number.replace("؟", "")
                card_number = card_number.replace("?", "")
                card_number = card_number.replace("%", "")
                nums = request.POST['numbers']
                user_select = User.objects.get(card_number=card_number)
                current_game = Game.objects.filter(user=user_select, end_time="00:00:00")
                if len(current_game):
                    credit_user = user_select.credit
                    current_game[0].end_time = datetime.datetime.now().time()

                    start = current_game[0].start_time
                    end = current_game[0].end_time
                    timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
                    if str(end) != "00:00:00":
                        yesterday = datetime.date.today() - datetime.timedelta(1)
                        timedelta_start_of_the_day = datetime.timedelta(hours=0, minutes=0, seconds=0)
                        timedelta_end_of_the_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
                        timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
                        if current_game[0].add_date == yesterday:
                            if end.hour == 0 or end.hour == 1 or end.hour == 2 or end.hour == 3:
                                t_one = timedelta_end_of_the_day - timedelta_start
                                t_two = timedelta_end - timedelta_start_of_the_day
                                point_one = int(round(t_one.total_seconds() / 225))
                                point_two = int(round(t_two.total_seconds() / 225))
                                point = point_one + point_two
                            else:
                                t_one = timedelta_end - timedelta_start
                                t_two = 0
                                point_one = int(round(t_one.total_seconds() / 225))
                                point_two = 0
                                point = point_one + point_two
                        else:
                            t = timedelta_end - timedelta_start
                            point = int(round(t.total_seconds() / 225))
                        credit = current_game[0].credit_used
                        price = point * 500 * current_game[0].numbers
                        if used_credit == "on":
                            if price >= credit_user:
                                current_game[0].credit_used = credit_user
                                user_select.credit = 0
                            else:
                                current_game[0].credit_used = price
                                user_select.credit = credit_user - price
                            user_select.save()
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
    yesterday = datetime.date.today() - datetime.timedelta(1)

    today_users = Game.objects.filter(add_date=datetime.datetime.now().date()).order_by('-end_time')
    yesterday_users = Game.objects.filter(add_date=yesterday).order_by('-end_time')
    for e in today_users:
        point = 0
        start = e.start_time
        end = e.end_time
        timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
        if str(end) != "00:00:00":
            timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
            t = timedelta_end - timedelta_start
            point = int(round(t.total_seconds() / 225))
            credit = e.credit_used
            users_list.append({'user_obj': e, "price": point * 500 * e.numbers, 'point': point * e.numbers, "end": 1,
                               "credit": credit})
    hour_of_now = datetime.datetime.now().hour
    if hour_of_now == 0 or hour_of_now == 1 or hour_of_now == 2 or hour_of_now == 3:
        for e in yesterday_users:
            point = 0
            start = e.start_time
            end = e.end_time
            timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
            timedelta_end_of_the_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
            if str(end) != "00:00:00":
                timedelta_start_of_the_day = datetime.timedelta(hours=0, minutes=0, seconds=0)
                timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
                if (end.hour == 0 or end.hour == 1 or end.hour == 2 or end.hour == 3) and (
                            start.hour != 0 and start.hour != 1 and start.hour != 2):
                    t_one = timedelta_end_of_the_day - timedelta_start
                    t_two = timedelta_end - timedelta_start_of_the_day
                    point_one = int(round(t_one.total_seconds() / 225))
                    point_two = int(round(t_two.total_seconds() / 225))
                    point = point_one + point_two
                else:
                    t_one = timedelta_end - timedelta_start
                    t_two = 0
                    point_one = int(round(t_one.total_seconds() / 225))
                    point_two = 0
                    point = point_one + point_two

                credit = e.credit_used
                users_list.append({'user_obj': e, "price": point * 500 * e.numbers,
                                   'point': point * e.numbers, "end": 1,
                                   "credit": credit})

    today_users_not_end = Game.objects.filter(add_date=datetime.datetime.now().date()).order_by('-start_time')
    yesterday_users_not_end = Game.objects.filter(add_date=yesterday).order_by('-start_time')
    for e in today_users_not_end:
        point = 0
        end = e.end_time
        if str(end) == "00:00:00":
            users_list.append(
                {'user_obj': e, "price": point * 500 * e.numbers, 'point': point * e.numbers, "end": 0, "credit": 0})
    for e in yesterday_users_not_end:
        point = 0
        end = e.end_time
        if str(end) == "00:00:00":
            users_list.append(
                {'user_obj': e, "price": point * 500 * e.numbers, 'point': point * e.numbers, "end": 0, "credit": 0})

    return render(request, 'addgame.html',
                  {"user_data": users_list, "is_done_addorstop": is_done_addorstop, "is_done_adduser": is_done_adduser,
                   'is_done_addcredit': is_done_addcredit})


def refine_users(request):
    all_users = User.objects.all()
    for user in all_users:
        cnum = user.card_number
        cnum = cnum.replace("?", "")
        cnum = cnum.replace("%", "")
        cnum = cnum.replace("؟", "")
        user.card_number = cnum
        user.save()


def delete_row(request):
    if request.method == "POST":
        deleted_row_id = request.POST['deleted_id']
        password = request.POST['password']
        if password == "zolzolzoli":
            row = Game.objects.get(pk=deleted_row_id)
            row.delete()
        return redirect('/addgame')


def user_info(request):
    if request.method == "POST":
        users_list = []
        sum_user = 0
        without_membership_price_variable = 0
        card_number = request.POST['card_id']
        card_number = card_number.replace("؟", "")
        card_number = card_number.replace("?", "")
        card_number = card_number.replace("%", "")
        user_data = Game.objects.filter(user__card_number=card_number)
        for e in user_data:
            start = e.start_time
            end = e.end_time
            timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
            if str(end) != "00:00:00":
                timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
                t = timedelta_end - timedelta_start
                point = int(round(t.total_seconds() / 225))
                sum_user += point * 500 * e.numbers
                if t.total_seconds() % 3600 > 900:
                    without_membership_point = int(t.total_seconds() / 3600) + 1
                    without_membership_price = without_membership_point * 8000 * e.numbers
                    without_membership_price_variable += without_membership_price
                else:
                    without_membership_point = int(t.total_seconds() / 3600)
                    without_membership_price = without_membership_point * 8000 * e.numbers
                    without_membership_price_variable += without_membership_price
                users_list.append(
                    {'user_obj': e, "price": point * 500 * e.numbers, 'point': point * e.numbers})

        return render(request, 'userinfo.html',
                      {"user_data": users_list, "sum": sum_user, "without": without_membership_price_variable,
                       "off": without_membership_price_variable - sum_user})
    return render(request, 'userinfo.html',
                  {})


def info(request):
    if request.method == "POST":
        if request.POST['search']:
            todate = request.POST['todate']
            todate_list = todate.split("/")
            fromdate = request.POST['fromdate']
            fromdate_list = fromdate.split("/")
            option = request.POST['option']
            if option == "monthly":
                data_chart = {"chart": {
                    "caption": "",
                    "subCaption": "",
                    "xAxisName": "Months",
                    "yAxisName": "Price",
                    "captionFontSize": "14",
                    "subcaptionFontSize": "14",
                    "baseFontColor": "#333333",
                    "baseFont": "Helvetica Neue,Arial",
                    "subcaptionFontBold": "0",
                    "paletteColors": "#6baa01,#008ee4",
                    "usePlotGradientColor": "0",
                    "bgColor": "#ffffff",
                    "showBorder": "0",
                    "showPlotBorder": "0",
                    "showValues": "0",
                    "showShadow": "0",
                    "showAlternateHGridColor": "0",
                    "showCanvasBorder": "0",
                    "showXAxisLine": "1",
                    "xAxisLineThickness": "1",
                    "xAxisLineColor": "#999999",
                    "canvasBgColor": "#ffffff",
                    "divlineAlpha": "100",
                    "divlineColor": "#999999",
                    "divlineThickness": "1",
                    "divLineDashed": "1",
                    "divLineDashLen": "1",
                    "legendBorderAlpha": "0",
                    "legendShadow": "0",
                    "toolTipColor": "#ffffff",
                    "toolTipBorderThickness": "0",
                    "toolTipBgColor": "#000000",
                    "toolTipBgAlpha": "80",
                    "toolTipBorderRadius": "2",
                    "toolTipPadding": "5"
                },
                    "categories": [
                        {
                            "category": [

                            ]
                        }
                    ],
                    "dataset": [
                        {
                            "seriesname": "Real Price",
                            "data": [

                            ]
                        },
                        {
                            "seriesname": "OFF Price",
                            "data": [

                            ]
                        }
                    ]
                }
                data = {"months": [], "sums": []}
                from_year = int(fromdate_list[2])
                from_year_copy = from_year
                to_year = int(todate_list[2])
                from_month = int(fromdate_list[0])
                to_month = int(todate_list[0])
                flag = 0
                for j in range(from_year, to_year + 1):
                    if from_year_copy != to_year and flag == 0:
                        to_month = 12
                        from_year_copy += 1
                        flag = 1
                    elif from_year_copy == to_year and flag == 0:
                        to_month = int(todate_list[0])
                        from_year_copy += 1
                        flag = 1
                    elif from_year_copy != to_year and flag == 1:
                        from_month = 1
                        to_month = 12
                        from_year_copy += 1
                        flag = 0
                    elif from_year_copy == to_year and flag == 1:
                        from_month = 1
                        to_month = int(todate_list[0])
                        from_year_copy += 1
                        flag = 0

                    for i in range(from_month, to_month + 1):
                        without_membership_price_variable = 0
                        j_date = jdatetime.date.fromgregorian(day=1, month=i, year=j)
                        data_chart['categories'][0]['category'].append(
                            {'label': str(j_date).split("-")[0] + "-" + str(j_date).split("-")[1]})
                        data['months'].append(str(j) + "-" + str(i))
                        targets = Game.objects.filter(add_date__month=i, add_date__year=j)
                        sum_month = 0
                        for target in targets:
                            start = target.start_time
                            end = target.end_time
                            timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute,
                                                                 seconds=start.second)
                            if str(end) != "00:00:00":
                                timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute,
                                                                   seconds=end.second)
                                t = timedelta_end - timedelta_start
                                point = int(round(t.total_seconds() / 225))
                                sum_month += point * 500 * target.numbers
                                if t.total_seconds() % 3600 > 900:
                                    without_membership_point = int(t.total_seconds() / 3600) + 1
                                    without_membership_price = without_membership_point * 8000 * target.numbers
                                    without_membership_price_variable += without_membership_price
                                else:
                                    without_membership_point = int(t.total_seconds() / 3600)
                                    without_membership_price = without_membership_point * 8000 * target.numbers
                                    without_membership_price_variable += without_membership_price

                        data_chart['dataset'][0]['data'].append({'value': sum_month})
                        data_chart['dataset'][1]['data'].append(
                            {'value': without_membership_price_variable - sum_month})
                        data['sums'].append(sum_month)

                line = FusionCharts("msarea", "ex1", "1200", "400", "chart-1", "json", data_chart)

                return render(request, 'multichart.html', {'output': line.render(), 'chartTitle': 'BoardGames Chart'})

            elif option == "weekly":
                pass
            elif option == "daily":
                data_chart = {"chart": {
                    "caption": "",
                    "subCaption": "",
                    "xAxisName": "Days",
                    "yAxisName": "Price",
                    "captionFontSize": "14",
                    "subcaptionFontSize": "14",
                    "baseFontColor": "#333333",
                    "baseFont": "Helvetica Neue,Arial",
                    "subcaptionFontBold": "0",
                    "paletteColors": "#6baa01,#008ee4",
                    "usePlotGradientColor": "0",
                    "bgColor": "#ffffff",
                    "showBorder": "0",
                    "showPlotBorder": "0",
                    "showValues": "0",
                    "showShadow": "0",
                    "showAlternateHGridColor": "0",
                    "showCanvasBorder": "0",
                    "showXAxisLine": "1",
                    "xAxisLineThickness": "1",
                    "xAxisLineColor": "#999999",
                    "canvasBgColor": "#ffffff",
                    "divlineAlpha": "100",
                    "divlineColor": "#999999",
                    "divlineThickness": "1",
                    "divLineDashed": "1",
                    "divLineDashLen": "1",
                    "legendBorderAlpha": "0",
                    "legendShadow": "0",
                    "toolTipColor": "#ffffff",
                    "toolTipBorderThickness": "0",
                    "toolTipBgColor": "#000000",
                    "toolTipBgAlpha": "80",
                    "toolTipBorderRadius": "2",
                    "toolTipPadding": "5"
                },
                    "categories": [
                        {
                            "category": [

                            ]
                        }
                    ],
                    "dataset": [
                        {
                            "seriesname": "Real Price",
                            "data": [

                            ]
                        },
                        {
                            "seriesname": "OFF Price",
                            "data": [

                            ]
                        }
                    ]
                }
                daily_data = {}
                targets = Game.objects.filter(add_date__range=(
                    fromdate_list[2] + "-" + fromdate_list[0] + "-" + fromdate_list[1],
                    todate_list[2] + "-" + todate_list[0] + "-" + todate_list[1]))
                for target in targets:
                    start = target.start_time
                    end = target.end_time
                    timedelta_start = datetime.timedelta(hours=start.hour, minutes=start.minute,
                                                         seconds=start.second)
                    if str(end) != "00:00:00":
                        timedelta_end = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
                        t = timedelta_end - timedelta_start
                        point = int(round(t.total_seconds() / 225))
                        price = point * 500 * target.numbers
                        if t.total_seconds() % 3600 > 0:
                            without_memebership_point = int(t.total_seconds() / 3600) + 1

                            without_memebership_price = without_memebership_point * 8000 * target.numbers
                        else:
                            without_memebership_point = int(t.total_seconds() / 3600)

                            without_memebership_price = without_memebership_point * 8000 * target.numbers

                        if str(target.add_date) in daily_data:
                            daily_data[str(target.add_date)][0] += price
                            daily_data[str(target.add_date)][1] += target.numbers
                            daily_data[str(target.add_date)][2] += without_memebership_price
                        else:
                            daily_data[str(target.add_date)] = [price, target.numbers, without_memebership_price]

                for e in sorted(daily_data.items()):
                    greg_date = e[0].split("-")
                    j_date = jdatetime.date.fromgregorian(day=int(greg_date[2]), month=int(greg_date[1]),
                                                          year=int(greg_date[0]))
                    data_chart['categories'][0]['category'].append({'label': str(j_date) + " ( " + str(e[1][1]) + " )"})
                    data_chart['dataset'][0]['data'].append({'value': e[1][0]})
                    data_chart['dataset'][1]['data'].append({'value': e[1][2] - e[1][0]})
                line = FusionCharts("msarea", "ex1", "1200", "400", "chart-1", "json", data_chart)

                return render(request, 'multichart.html', {'output': line.render(), 'chartTitle': 'BoardGames Chart'})

    return render(request, 'info.html', {})
