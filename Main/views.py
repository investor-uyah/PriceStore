# prices/views.py
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Members, Price
from django.db.models import Count, Avg, Min, Max
from . import forms
import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
import random

# Create your views here.
# These views are fine and don't need changes.
def details(request, id):
    memberid = Members.objects.get(id=id) 
    template = loader.get_template('details.html')
    context = {
        'memberid': memberid
    }
    return HttpResponse(template.render(context, request))

@login_required
def main(request):
    return render(request, 'main.html')

@login_required
def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            name = form.cleaned_data.get('name', '')
            
            send_mail(
                name,
                topic,
                message, 
                sender,
                ['investor@gmail.com']
            )
        return redirect('main')
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required
def search_view(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        entry = Price.objects.filter(foodstuff__icontains=searched)
        return render(request, 'search_page.html', {'searched': searched, 'entry': entry})
    else: 
        return render(request, 'main.html')

@login_required
def about(request):
    return render(request, "about.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect("main")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request, "registration/login.html")
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def purchase(request):
    if request.method == 'POST':
        form = forms.PurchaseForm(request.POST)
        if form.is_valid():
            new_price = form.save(commit=False)
            new_price.author = request.user
            new_price.save()
            messages.success(request, "Your operation was successful!")
            return redirect('prices')
    else:
        form = forms.PurchaseForm(initial={'day': datetime.date.today()})
    return render(request, 'purchaseupdate.html', {'form': form})

# This is the single, combined view for price_page.html
@login_required
def prices_combined(request):
    # Logic for "Prices Across Nigeria"
    prices = Price.objects.all().order_by('-id')
    locations = Price.objects.values('state').distinct()
    locations_list = list(locations)
    random.shuffle(locations_list)
    locations_list = (locations_list)[:5]

    # Logic for "States-based Prices"
    prices_by_state = Price.objects.values("state").annotate(Total=Count("id"))

    # Logic for "Price Summary" (cheapest/expensive)
    cheapest = Price.objects.values('foodstuff').annotate(min_price=Min('price')).order_by('min_price')[:3]
    expensive = Price.objects.values('foodstuff').annotate(max_price=Max('price')).order_by('-max_price')[:3]

    # Logic for "Price Trends"
    today = datetime.date.today()
    this_week_start = today - datetime.timedelta(days=7)
    last_week_start = today - datetime.timedelta(days=14)
    items = ["Rice", "Beans", "Yam", "Garri"]
    trends = {}

    for item in items:
        current_price_query = Price.objects.filter(
            foodstuff__iexact=item,
            created_at__gte=this_week_start,
            created_at__lte=today
        ).aggregate(avg=Avg("price"))
        
        previous_price_query = Price.objects.filter(
            foodstuff__iexact=item,
            created_at__gte=last_week_start,
            created_at__lt=this_week_start
        ).aggregate(avg=Avg("price"))

        current_price = current_price_query.get('avg')
        previous_price = previous_price_query.get('avg')

        if current_price is not None and previous_price is not None and previous_price > 0:
            change = ((current_price - previous_price) / previous_price) * 100
            if change > 2:
                status = f"🔺 +{round(change, 1)}%"
            elif change < -2:
                status = f"🔻 {round(change, 1)}%"
            else:
                status = "✅ stable"
        else:
            status = "No data available."
        trends[item] = status
        
    # NEW: Logic for 'Average Food Prices'
    food_items = Price.objects.all().values('foodstuff', 'price')
    
    # Calculate average price for each foodstuff
    from collections import defaultdict
    summary = defaultdict(lambda: {'total': 0, 'count': 0})
    for item in food_items:
        summary[item['foodstuff']]['total'] += item['price']
        summary[item['foodstuff']]['count'] += 1

    # Format the summary for the template
    average_prices = {
        food: {
            'average': summary[food]['total'] // summary[food]['count'],
            'total_listings': summary[food]['count']
        }
        for food in summary
    }


    return render(request, 'price_page.html', {
        'prices': prices,
        'locations': locations,
        'locations_list': locations_list,
        'prices_by_state': prices_by_state,
        'cheapest': cheapest,
        'expensive': expensive,
        'trends': trends,
        'average_prices': average_prices,
    })

@login_required
def states_listing(request, state):
    prices = Price.objects.filter(state=state)
    return render(request, 'state_listing.html', {
        'state': state,
        'prices': prices
    })
