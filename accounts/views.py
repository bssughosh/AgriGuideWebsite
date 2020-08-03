import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, auth
from django.contrib import messages

import pandas as pd
import os

from ProjectWebsite.settings import MEDIA_ROOT

from .models import UserData
from .verhoeff import *


# Create your views here.
def home(request):
    return render(request, 'homepage.html')


def login1_1(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if UserData.objects.filter(mobile=phone).exists():
            api_key = '53f61d41fb8efac0683ac757ef908d367be1f538'
            ph = '+91' + str(phone)
            url = 'https://api.ringcaptcha.com/la3a3adu8idi7a5aho9y/code/sms'
            params = {
                'phone': ph,
                'api_key': api_key
            }
            r = requests.post(url, params=params).json()
            if r['status'] == 'ERROR':
                messages.error(request, 'An error occurred. Please try again.')
            elif r['status'] == 'SUCCESS':
                return redirect('/login/' + phone)
        else:
            messages.warning(request, f'Phone number {phone} not registered. Continue to Sign up page?')

    return render(request, 'accounts/login.html')


def login1(request, ph):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        api_key = '53f61d41fb8efac0683ac757ef908d367be1f538'
        pho = '+91' + str(phone)
        url = 'https://api.ringcaptcha.com/la3a3adu8idi7a5aho9y/verify'
        params = {
            'phone': pho,
            'api_key': api_key,
            'code': otp,
        }
        r = requests.post(url, params=params).json()
        if r['status'] == 'SUCCESS':
            u = authenticate(request, username=phone, password='12345')
            if u is not None:
                login(request, u)
                return redirect('/')
        elif r['status'] == 'ERROR':
            messages.error(request, 'An error occurred. Please try again.')
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
    user = UserData.objects.get(id=obj)

    if request.method == 'POST':
        aadhar = request.POST.get('aadhar')
        if UserData.objects.filter(aadhar=aadhar).exists():
            messages.warning(request,
                             f"Aadhar number {aadhar} already registered. Do you want to login using some other number?")

        else:
            if validateVerhoeff(aadhar):
                user.aadhar = aadhar
                user.save()

                u = User.objects.create_user(username=user.mobile, password='12345', first_name=user.name)
                auth.login(request, u)
                return redirect('/')
            else:
                messages.error(request, 'Aadhar card number is wrong!')

    return render(request, 'accounts/reg3.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')
