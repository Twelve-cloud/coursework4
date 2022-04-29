import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import request
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from math import *
from .models import *
from .helpers import *


def index(request):
    if request.user.is_authenticated:
        user = request.user
        userStocks = Stock.objects.filter(owner=user)
        data = [stock.serialize() for stock in userStocks]
        return render(request, "broker/index.html", {'data': data})
    else:
        return HttpResponseRedirect(reverse("login"))


def corpRedirect(request, symbol):
    data = get_company(symbol)
    return render(request, "broker/corp.html", {
        'symbol': symbol,
        'data': data,
    })


def charts(request):
    return render(request, "broker/charts.html")


@csrf_exempt
def orders(request):
    username = [x.username for x in Request.objects.all()]
    comp_name = [x.company for x in Request.objects.all()]
    prices = [x.price for x in Request.objects.all()]
    types = [x.type for x in Request.objects.all()]
    or_data = []

    for u, c, p, t in zip(username, comp_name, prices, types):
        or_data.append({'username': u, 'company': c, 'price': p, 'type': t})

    if request.method == 'PUT' and b"delete" not in request.body:
        d = eval(request.body)
        username = d["username"]
        company = d["company"]
        type = d["type"]
        price = d["price"]
        price = float(price[:-3])
        Request.objects.create(
            username=username,
            company=company,
            type=type,
            price=price
        )
    elif request.method == 'PUT' and b"delete" in request.body:
        d = eval(request.body)
        username = d["username"]
        company = d["company"]
        dat = Request.objects.filter(username=username, company=company)
        dat.delete()
    return render(request, "broker/orders.html", {"data": or_data})


@csrf_exempt
def personal_data(request):
    if request.method == 'PUT':
        d = eval(request.body)
        username = d["username"]
        email = d["email"]
        password = d["password"]
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.save()
    else:
        return render(request, "broker/personal_data.html")


comp_name = [x.name for x in Company.objects.all()]
prices = [x.price for x in Service.objects.all()]
types = ['Покупка акций' for x in range(len(comp_name))]
data = []

for c, p, t in zip(comp_name, prices, types):
    data.append({'company': c, 'price': p, 'type': t})


def services(request):
    return render(request, "broker/services.html", {"data": data})


# API_METHODS
@login_required
def broker_data(request):
    username = request.user.username
    user = User.objects.get(username=username)
    s = user.serialize()
    balance = getBalance(username)
    dataPoint = DataPoint(y=balance, owner=user)
    dataPoint.save()

    x = [point.x.strftime("%b %-d %Y, %-I:%M %p")
         for point in DataPoint.objects.filter(owner=user)]
    y = [point.y for point in DataPoint.objects.filter(owner=user)]

    changePer = round(
        ((balance - user.initial_balance) / user.initial_balance) * 100, 4
    )
    data = {
        'x': x,
        'y': y,
        'balance': round(balance, 2),
        'changePer': changePer
    }
    return JsonResponse(data, safe=False)


def symbols(request):
    data = get_symbols()
    return JsonResponse(data, safe=False)


def corpData(request, symbol):
    data = stats(symbol=symbol)
    Smax = round(max([d['close'] for d in data['chart'] if d['close']]))

    sMax = ((Smax // (10**floor(log10(Smax)))) + 1) * 10**floor(log10(Smax))
    return JsonResponse({
        'data': data['chart'],
        'sMax': sMax,
        'lastUpdated': data['lastUpdated'],
        'latestPrice': data['lastPrice']
    }, safe=False)


# buy a stock
@csrf_exempt
@login_required
def buy(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required."}, status=400)
    user = request.user

    userSerial = user.serialize()
    data = json.loads(request.body)

    symbol = data.get('symbol', "")
    price = data.get('price', "")
    message = ''
    if(user.current_balance >= price):

        stock = Stock(symbol=symbol, buy_price=price, owner=user)
        stock.save()
        # save datapoint
        # BOTTLE NECK TAKES ALOT OF TIME
        # inORDER TO [QUOTE] EACH STOCK
        user.current_balance -= price
        print("\n\n blnc: ", user.current_balance)
        user.save()
        blnc = getBalance(user.username)
        print("\n\n dPblnc: ", blnc)
        dataPoint = DataPoint(y=blnc, owner=user)
        dataPoint.save()
        message = 'Куплено успешно'
    else:
        message = 'Transaction Failed'

    return JsonResponse({'message': message}, safe=0)


# buy a stock
@csrf_exempt
@login_required
# BUGs
def sell(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required."}, status=400)
    user = request.user
    data = json.loads(request.body)
    # get the stock
    stockId = data.get('id', "")
    message = ''

    stock = Stock.objects.get(id=stockId)
    stockSer = stock.serialize()
    priceNow = quote([stockSer['symbol']])
    dif = priceNow - float(stockSer['buy_price'])

    user.current_balance += dif
    stock.delete()
    user.save()
    # save datapoint
    # BOTTLE NECK TAKES ALOT OF TIME
    # inORDER TO [QUOTE] EACH STOCK
    dataPoint = DataPoint(y=getBalance(user.username), owner=user)
    dataPoint.save()

    message = 'Продано успешно'

    return JsonResponse({'message': message}, safe=0)


# authentication functionality
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if user.category == 'U':
                return HttpResponseRedirect(reverse("services"))
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "broker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "broker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "broker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "broker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "broker/register.html")
