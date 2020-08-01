import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

import pandas as pd
import os

from django.utils.safestring import mark_safe

from ProjectWebsite.settings import MEDIA_ROOT

from .models import UserData
from .verhoeff import *


# Create your views here.
def home(request):
    return render(request, 'homepage.html')


def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        return redirect(phone + '/')

    return render(request, 'accounts/login.html')


def login1(request, ph):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')

    return render(request, 'accounts/login_verify.html', {'phone': ph})


def reg_state(request):
    return redirect('/register/andhra+pradesh/adilabad/')


def place_transformation(label):
    s = label.upper()
    s = s.replace('+', ' ')
    return s


def forward_state(request, state):
    file = os.path.join(MEDIA_ROOT, 'support_data', 'places.csv')
    df = pd.read_csv(file)
    fil = df[df['State'] == state]
    dists = list(fil['District'].unique())
    return redirect(f'/register/{state}/{dists[0]}')


def reg1(request, state, dist):
    file = os.path.join(MEDIA_ROOT, 'support_data', 'places.csv')
    df = pd.read_csv(file)
    states = list(df['State'].unique())
    fil = df[df['State'] == state]
    dists = list(fil['District'].unique())
    states_disp1 = df['State'].apply(lambda x: place_transformation(x))
    states_disp = list(states_disp1.unique())
    dists_disp = list(fil['District'].apply(lambda x: place_transformation(x)))

    if request.method == 'POST':
        n = request.POST.get('name')
        a = request.POST.get('address')
        p = request.POST.get('pincode')

        user_data = UserData.objects.create(name=n, add1=a, pincode=p, state=state, district=dist)

        return redirect(f'/register2/{user_data.id}')
    return render(request, 'accounts/reg1.html',
                  {'states': states, 'dists': dists, 'state': state, 'dist': dist, 's_d': states_disp,
                   'd_d': dists_disp})


def reg2(request, obj):
    user = UserData.objects.get(id=obj)

    if request.method == 'POST' and 'getter' in request.POST:
        ph = request.POST.get('phone')

        if UserData.objects.filter(mobile=ph).exists():
            messages.warning(request, f"Phone number {ph} already registered. Do you want to login?")
        else:
            api_key = '53f61d41fb8efac0683ac757ef908d367be1f538'
            pho = '+91' + str(ph)

            url = 'https://api.ringcaptcha.com/la3a3adu8idi7a5aho9y/code/sms'
            params = {
                'phone': pho,
                'api_key': api_key
            }
            r = requests.post(url, params=params).json()
            if r['status'] == 'ERROR':
                messages.error(request, 'An error occurred. Please try again.')
            elif r['status'] == 'SUCCESS':
                return render(request, 'accounts/reg2.html', {'tog': 0, 'obj': obj, 'ph': ph})

    elif request.method == 'POST':
        ph = request.POST.get('phone')
        otp = request.POST.get('otp')

        api_key = '53f61d41fb8efac0683ac757ef908d367be1f538'
        pho = '+91' + str(ph)
        url = 'https://api.ringcaptcha.com/la3a3adu8idi7a5aho9y/verify'
        params = {
            'phone': pho,
            'api_key': api_key,
            'code': otp,
        }
        r = requests.post(url, params=params).json()
        if r['status'] == 'SUCCESS':
            user.mobile = int(ph)
            user.save()
            return redirect(f'/register3/{obj}/')
        elif r['status'] == 'ERROR':
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'accounts/reg2.html', {'tog': 0, 'obj': obj, 'ph': ph})

    return render(request, 'accounts/reg2.html', {'tog': 1, 'obj': obj})


def deleter(request, obj):
    UserData.objects.filter(id=obj).delete()
    return redirect('/login/')


def deleter1(request, obj):
    UserData.objects.filter(id=obj).delete()
    return redirect('/')


def reg3(request, obj):

    return render(request, 'accounts/reg3.html')
