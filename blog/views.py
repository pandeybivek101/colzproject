from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import Http404
from django.http import *
from .models import Destination
from django.db.models import Q
from .forms import DurationForm
from math import sin, cos, sqrt, atan2, radians
from scipy import spatial
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from account.models import UserHistory

#filter places radio TextInput
def FilterPlacesRadioInput(send):
    places = Destination.objects.filter(
    Q(trekking_type__contains = send['trekking']), Q(destinaton_type__contains = send['destination']), Q(accomodation_type__contains = send['accomodation'])
    )
    radiofilterplace = []
    for p in places:
        radiofilterplace.append(p.title)
    return radiofilterplace


def ApplyCosineSimi(cosine_para, places):
    #print(cosine_para)
    allnumlist = [int(x) for x in cosine_para]
    print(allnumlist)
    data = Destination.objects.filter(title__in = places)
    result1=[]
    for d in data:
        place = [d.temperature, d.difficulty, d.security]
        #print(place)
        result = (1 - spatial.distance.cosine(place, allnumlist)) * 100
        result1.append(float("{0:.2f}".format(result)))
    #print(result1)
    return result1

def HomePage(request):
    return render(request, 'blog/index.html',{'title':"GO Travellers | Home"})


def PostDetails(request, id):
    place = Destination.objects.get(id=id)
    return render(request, 'blog/post.html', {"thispost": place,'title':"GO Travellers | Destination Detail"})



def Recommendation(request):
    form = DurationForm()
    return render(request, 'blog/recommendation.html', {'form': form})


def r_result(request):
    if request.method!="POST":  #add this
        return redirect('Recommendation') #add this
    elif request.method == 'POST': #edit if to elif 
        # print('aayo')
        form = DurationForm(request.POST)
        print(form.errors)
        print(form.non_field_errors)
        if form.is_valid():
            # print('ok to go')
            temperature = form.cleaned_data['temperature']
            difficulty = form.cleaned_data['difficulty']
            security = form.cleaned_data['security']
            trekking = form.cleaned_data['trekking_type']
            destination = form.cleaned_data['destination_type']
            accomodation = form.cleaned_data['accomodation_type']
            places = Destination.objects.all()
            duration = form.cleaned_data['duration']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            if request.user.is_authenticated:
                UserHistory.objects.get_or_create(duration = duration, trekking_type = trekking, 
                    destination_type = destination, accomodation_type = accomodation, 
                    temperature = temperature, difficulty = difficulty, security = security,
                    latitude = latitude, longitude = longitude, user = request.user)
            #print(latitude)
            #print(longitude)
            data = []
            try:
                for place in places:
                    R = 6371.0
                    name = place.title
                    lat1 = radians(place.latitude)
                    lon1 = radians(place.longitude)

                    # print(latitude)
                    lat2 = radians(latitude)
                    lon2 = radians(longitude)

                    # print(longitude)
                    dlon = lon2 - lon1
                    dlat = lat2 - lat1

                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    distance = R * c

                    if distance <= int(duration):
                        data.append(name)
            except TypeError:
                print("May be GPS is not ON. Please Trun it ON")

            finally:
                send = {'trekking':trekking, 'destination': destination, 'accomodation': accomodation}
                data_for_cosine = [temperature, difficulty, security]
                # print(data_for_cosine)
                filteredplaces = FilterPlacesRadioInput(send)
                # print(data)

                if len(data) == 0:
                    cosine_data = ApplyCosineSimi(data_for_cosine, filteredplaces)
                    finaldestination = Destination.objects.filter(title__in = cosine_data[1])
                    print(cosine_data[1])

                else:
                    common = set(data).intersection(set(filteredplaces))
                    cosine_data = ApplyCosineSimi(data_for_cosine, common)
                    finaldestination = Destination.objects.filter(title__in = cosine_data[1])



                gogo = {'places': finaldestination,'cosine':cosine_data[0],'title':"GO Travellers | Recommendation"}
                return render(request, 'blog/r_result.html', gogo)
        else:
            form = DurationForm()
            UserVisitedForm()
            return HttpResponseRedirect('/recommendation/')


import random
@login_required
def Search(request):
    userid = request.user.id
    print(userid)
    if not userid:
        finaldestination = []
        gogo = {'places': finaldestination ,'title':"GO Travellers | Recommended For You"}
        return render(request, 'blog/search.html', gogo)
    else:
        #obj = UserHistory.objects.filter(user_id=userid).latest('id')
        obj = random.choice(list(UserHistory.objects.filter(user_id=userid)))
        print(obj)
        if obj:
            temperature = obj.temperature
            difficulty = obj.difficulty
            security = obj.security
            trekking = obj.trekking_type
            destination = obj.destination_type
            accomodation = obj.accomodation_type
            places = Destination.objects.all()
            duration = obj.duration
            latitude = obj.latitude
            longitude = obj.longitude
            data = []
            try:
                for place in places:
                    R = 6371.0
                    name = place.title
                    lat1 = radians(place.latitude)
                    lon1 = radians(place.longitude)
                    # print(latitude)
                    lat2 = radians(latitude)
                    lon2 = radians(longitude)
                    # print(lat1)

                    dlon = lon2 - lon1
                    dlat = lat2 - lat1

                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    distance = R * c

                    if distance <= int(duration):
                        data.append(name)
            finally:
                send = {'trekking':trekking, 'destination': destination, 'accomodation': accomodation}
                data_for_cosine = [temperature, difficulty, security]
                filteredplaces = FilterPlacesRadioInput(send)

                if len(data) == 0:
                    cosine_data = ApplyCosineSimi(data_for_cosine, filteredplaces)
                    finaldestination = Destination.objects.filter(title__in = cosine_data[1])
                    print(cosine_data)

                else:
                    common = set(data).intersection(set(filteredplaces))
                    cosine_data = ApplyCosineSimi(data_for_cosine, common)
                    finaldestination = Destination.objects.filter(title__in = cosine_data[1])

                gogo = {'places': finaldestination, 'cosine': cosine_data,'title':"GO Travellers | Recommended"}
                return render(request, 'blog/search.html', gogo)
