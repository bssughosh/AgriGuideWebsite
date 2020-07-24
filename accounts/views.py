from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

import pandas as pd
import os

from ProjectWebsite.settings import MEDIA_ROOT

from .models import UserData


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

    return render(request, 'accounts/reg1.html',
                  {'states': states, 'dists': dists, 'state': state, 'dist': dist, 's_d': states_disp,
                   'd_d': dists_disp})
