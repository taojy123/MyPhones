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

    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    if len(Phone.objects.filter(user=user)) >= 20:
        return HttpResponseRedirect("/")

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
    time = request.REQUEST.get("time", "")
    brand = request.REQUEST.get("brand", "")
    pattern = request.REQUEST.get("pattern", "")
    number = request.REQUEST.get("number", "")
    price_out = request.REQUEST.get("price_out", "")
    settled = request.REQUEST.get("settled", "")

    if time or brand or pattern or number or price_out or settled:
        filter_flag = "block"
    else:
        filter_flag = "none"


    rs = Phone.objects.order_by("-id")
    if not request.user.is_superuser:
        rs = rs.filter(user__icontains=request.user)

    if time:
        rs = rs.filter(time__icontains=time)

    if brand:
        rs = rs.filter(brand__icontains=brand)

    if pattern:
        rs = rs.filter(pattern__icontains=pattern)

    if number:
        rs = rs.filter(number__icontains=number)

    if price_out:
        rs = rs.filter(price_out__icontains=price_out)

    if settled:
        settled = eval(settled)
        rs = rs.filter(settled=settled)

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


@login_required(login_url="/loginpage")
def admin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("/")
    rs = User.objects.all()
    return render_to_response('admin.html', locals())


@login_required(login_url="/loginpage")
def setpwd(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("/")
    id = request.REQUEST.get("id")
    pwd = request.REQUEST.get("pwd")
    user = User.objects.get(id=id)
    user.set_password(pwd)
    user.save()
    return HttpResponseRedirect("/admin")


@login_required(login_url="/loginpage")
def setadmin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("/")
    id = request.REQUEST.get("id")
    user = User.objects.get(id=id)
    user.is_superuser = True
    user.save()
    return HttpResponseRedirect("/admin")


@login_required(login_url="/loginpage")
def user_del(request):
    id = request.REQUEST.get("id")
    User.objects.filter(id=id).delete()
    return HttpResponseRedirect("/admin")




#==================== auth ===========================================

def loginpage(request):
    return render_to_response('loginpage.html', locals())

def registerpage(request):
    return render_to_response('registerpage.html', locals())

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
    msg = ""
    username = request.REQUEST.get('username')
    password1 = request.REQUEST.get('password1')
    password2 = request.REQUEST.get('password2')
    if username and password1 and password2:
        if User.objects.filter(username=username):
            msg = "该用户名已被注册"
            return render_to_response('registerpage.html', locals())
        if password1 == password2:
            user = User()
            user.username = username
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect("/")
    msg = "输入有误，请重新输入"
    return render_to_response('registerpage.html', locals())

#======================================================================
