# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from models import *
import os
import uuid


@login_required(login_url="/loginpage")
def index(request):
    show_time = time.strftime("%Y-%m-%d")
    return render_to_response('index.html', locals())


@login_required(login_url="/loginpage")
def phone_add(request):
    time = request.REQUEST.get("time")
    brand = request.REQUEST.get("brand")
    pattern = request.REQUEST.get("pattern")
    sn = request.REQUEST.get("sn")
    price_in = request.REQUEST.get("price_in")
    number = request.REQUEST.get("number")
    price_out = request.REQUEST.get("price_out")
    time_out = request.REQUEST.get("time_out")
    settled = request.REQUEST.get("settled", False)
    remark = request.REQUEST.get("remark")

    if time:
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
    else:
        time = None

    if time_out:
        time_out = datetime.datetime.strptime(time_out, "%Y-%m-%d")
    else:
        time_out = None

    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    phone = Phone()
    phone.user = user
    phone.time = time
    phone.brand = brand
    phone.pattern = pattern
    phone.sn = sn
    phone.price_in = price_in
    phone.number = number
    phone.price_out = price_out
    phone.time_out = time_out
    phone.settled = settled
    phone.remark = remark
    phone.save()

    return HttpResponseRedirect("/")


@login_required(login_url="/loginpage")
def phones(request):
    rs = Phone.objects.order_by("-id")
    return render_to_response('phones.html', locals())


@login_required(login_url="/loginpage")
def phone_del(request):
    id = request.REQUEST.get("id")
    Phone.objects.filter(id=id).delete()
    return HttpResponseRedirect("/phones")


@login_required(login_url="/loginpage")
def phone_settled(request):
    id = request.REQUEST.get("id")
    phone = Phone.objects.get(id=id)
    phone.settled = True
    phone.save()
    return HttpResponseRedirect("/phones")


@login_required(login_url="/loginpage")
def phone_unsettled(request):
    id = request.REQUEST.get("id")
    phone = Phone.objects.get(id=id)
    phone.settled = False
    phone.save()
    return HttpResponseRedirect("/phones")





#==================== auth ===========================================

def loginpage(request):
    return render_to_response('loginpage.html', locals())

def login(request):
    username = request.REQUEST.get('username', '')
    password = request.REQUEST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    return HttpResponseRedirect("/")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")

def register(request):
    username = request.REQUEST.get('username')
    password1 = request.REQUEST.get('password1')
    password2 = request.REQUEST.get('password2')
    if username and password1 and password2:
        user = user()
        user.username = username
        user.password = password1
        user.save()
    return HttpResponseRedirect("/")

#======================================================================
