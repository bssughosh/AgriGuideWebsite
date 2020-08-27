from django.shortcuts import render, redirect
from accounts.models import UserData


# Create your views here.
def show_results(request):
    # user_data = UserData.objects.get(mobile=request.user.get_username())
    # dist = user_data.district
    # state = user_data.state
    # TODO: Update the state and dist to User Data Values and input start and end
    state = ''
    dist = ''
    start = 6
    end = 10
    return render(request, 'weather/first_page.html', {'state': state, 'dist': dist, 'start': start, 'end': end})
