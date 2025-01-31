from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Memebers
from .models import Price
# from .forms import PurchaseForm
# from .forms import StoreForm
from django.db.models import Count
from . import forms
import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

count = 0

# Create your views here.
# @login_required
# def members(request):
#    mymembers = Memebers.objects.all().values()
#    template = loader.get_template('myfirst.html')
#    context = {
#    'mymembers' : mymembers,
#    }

#    return HttpResponse(template.render(context, request))

#@login_required
def details(request, id):
    memberid = Memebers.objects.get(id=id) 
    template = loader.get_template('details.html')
    context = {
        'memberid': memberid
    }
    return HttpResponse(template.render(context, request))

@login_required
def main(request):
    template = loader.get_template('main.html')
    context = {
        'main' : main,
    }
    return HttpResponse(template.render(context, request))

@login_required
def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
           topic = form.cleaned_data['topic']
           message = form.cleaned_data['message']
           sender = form.cleaned_data.get('sender', 'noreply@example.com')

           send_mail (
                name,
                topic,
                message, 
                sender,
                ['investor@gmail.com']
            )
        return redirect('main')
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html/', {'form':forms.ContactForm})    

@login_required
def search_view(request):
    if request.method == 'POST':
        
        searched = request.POST['searched']
        entry = Price.objects.filter(name_contains=searched)
        return render(request, 'search_page.html/', {'searched':searched}, {'entry':entry})
    else: 
        return render(request, 'main.html/')

@login_required
def about(request):
    return render(request, "about.html")


# def contact(request):
    template = loader.get_template('contact.html')
    context = {
        'form': forms.ContactForm,
    }
    return HttpResponse(template.render(context, request))


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:

        auth.login(request, user)

        return HttpResponseRedirect("/account/loggedin/")
    else:
        return HttpResponseRedirect("/account/invalid/")

def logout(request):
    auth.logout(request)
    # redirect to a success page
    return HttpResponseRedirect("/account/loggedout/")

@login_required
def purchase(request):
    if request.method == 'POST':
        form = forms.PurchaseForm(request.POST)
        if form.is_valid():
            new_price = form.save(commit=False)
            new_price.author = request.user
            new_price.save()
            messages.success = (request, "Your operation was successful!")
            return redirect('prices')
    else:
        form=forms.PurchaseForm(initial={'day': datetime.date.today()})
    
    return render(request, 'purchaseupdate.html/', {'form':forms.PurchaseForm})

@login_required
def prices(request):
    prices = Price.objects.all().order_by('-id')
    return render(request, 'price_page.html/', {'prices': prices})

@login_required
def location(request):
    locations = Price.objects.values('state').distinct()
    return render(request, 'price_page.html/', {'locations': locations})

@login_required
def food_count(request):

    # Iterate over the Price objects
    food_items = Price.objects.all().values('foodstuff', 'price')
    food_counts = list(food_items)

    # Pass the list as a Json object to the template
    return JsonResponse(food_counts, safe=False)