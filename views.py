from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
import requests
import datetime
from viewer.forms import SignUpForm, ServicesCreateForm
from django.views import View
from viewer.models import Profile, ChosenServices, Services
from django.forms import modelformset_factory


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ServicesFormSet = modelformset_factory(Services, fields=('name',), max_num=len([Services.objects]))
        formset = ServicesFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset}) #tu moge wiecej formularzy (queryste z bazy)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        ServicesFormSet = modelformset_factory(Services, fields=('name',))
        formset = ServicesFormSet(request.POST)

        if form.is_valid():

            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            u = form.cleaned_data
            p = Profile.objects.create(
                user=user,
                email=u['email'],
                first_name=u['first_name'],
                last_name=u['last_name'],
                date_of_birth=u['date_of_birth']
            )
            p.save()
            print(p)
            print(p.pk)
            s = formset.cleaned_data
            print(s)
            for _ in s:
                print(_)
                ChosenServices.objects.create(
                    service_id=_['id'],
                    user_id=p,

                )
            login(request, user)

        return redirect("home")


class ServicesCreateView(FormView):
    template_name = 'form.html'
    form_class = ServicesCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        output = super().form_valid(form)
        service = form.cleaned_data
        Services.objects.create(
            name=service['name'],
            description=service['description']
        )
        return output


def kitty():
    fact_url = 'https://cat-fact.herokuapp.com/facts/random'
    r = requests.get(fact_url)
    res = r.json()
    text = res['text']
    pic_url = 'http://placekitten.com/400/500'

    return {'pic': pic_url, 'fact': text}


def weather(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'London'

    appid = '6de08c50f8dd1b05ac6c4f3614388ce6'
    URL = 'http://api.openweathermap.org/data/2.5/weather'
    PARAMS = {'q':city, 'appid':appid, 'units':'metric'}
    r = requests.get(url=URL, params=PARAMS)
    res = r.json()
    description = res['weather'][0]['description']
    icon = res['weather'][0]['icon']
    temp = res['main']['temp']
    pressure = res['main']['pressure']
    wind = round(res['wind']['speed']*3.6, 2)

    day = datetime.date.today()

    return {'description': description, 'icon': icon,
                                        'temp': temp, 'day': day, 'city': city,
                                        'pressure': pressure, 'wind': wind}


def nameday():
    url = 'https://nameday.abalin.net/api/V1/today'
    r = requests.get(url).json()
    nameday = r['nameday']['pl']

    return {'nameday': nameday}


def chuck():
    url = 'https://api.chucknorris.io/jokes/random'
    r = requests.get(url).json()
    chuck = r['value']

    return {'chuck': chuck}


class HomeView(View):
    def get(self, request):

        if 'city' in request.POST:
            weather.city = request.POST['city']
        else:
            weather.city = 'London'

        return render(request, 'home.html', context={'kitty': kitty(), 'weather': weather(request),
                                                        'nameday': nameday(), 'chuck': chuck()})

    def post(self, request):
        if 'city' in request.POST:
            weather.city = request.POST['city']
        else:
            weather.city = 'London'

        return render(request, 'home.html', context={'kitty': kitty(), 'weather': weather(request),
                                                        'nameday': nameday(), 'chuck': chuck()})