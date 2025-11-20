# prices/views.py
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Members, Price, BlogPost
from django.db.models import Count, Avg, Min, Max, Q
from . import forms
import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MemberForm
from django_ratelimit.decorators import ratelimit
import random
import json
from openai import OpenAI
import logging
import os 
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from django.contrib.auth import get_user_model
import csv


User = get_user_model()


# Create your views here.
# These views are fine and don't need changes.
def details(request, id):
    memberid = Members.objects.get(id=id) 
    template = loader.get_template('details.html')
    context = {
        'memberid': memberid
    }
    return HttpResponse(template.render(context, request))

def main(request):
    return render(request, 'main.html')

# @login_required
#def mymember(request):
#    members = Member.objects.all()
#    return render(
 #       request,
 #       'stores-list.html',
 #       members
   # ) -->

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, "blog_list.html", {"posts": posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog_detail.html", {"post": post})

@login_required
def register_partner(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False) # Don't save yet
            member.user = request.user # Attach the logged-in user
            member.save() # Now save the object
            return redirect('prices') # Redirect to a success page
    else:
        form = MemberForm()
    
    context = {'form': form}
    return render(request, 'partner.html', context)

@login_required
def csv_download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="thepricemarketplace_food_prices.csv"'

    writer = csv.writer(response)
    writer.writerow(['Foodstuff', 'Price', 'Description', 'Market/Store', 'State', 'Date'])

    for item in Price.objects.all():
        writer.writerow([item.foodstuff, item.price, item.description, item.market_store_name, item.state, item.created_at])

    return response

def stores_list(request):
    members = Members.objects.all()
    return render(request, 'stores-list.html', {'members':members})

def privacy_policy(request):
    return render(request, 'privacy.html')

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


def search_view(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()
        
        entry = Price.objects.filter(
            Q(foodstuff__icontains=searched) |
            Q(market_store_name__icontains=searched) |
            Q(state__icontains=searched) |
            Q(price__icontains=searched) |
            Q(lga__icontains=searched) |
            Q(description__icontains=searched)
        )
        
        return render(request, 'search_page.html', {
            'searched': searched,
            'entry': entry
        })
    return render(request, 'main.html')

def about(request):
    return render(request, "about.html")

def add_to_cart(request, id):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")

        # define cart
        cart = request.session.setdefault("cart", {})

        # increment product qty in cart when one exists
        if str(id) in cart:
            cart[str(id)]["qty"] += 1
        
        # create new cart otherwise
        else:
            cart[str(id)] = {
                "name": name,
                "price": price,
                "qty": 1,
            }
        
        request.session.modified = True

        # ✅ Success message
        messages.success(request, f"{name} has been added to your cart!")

        # Don't redirect to view_cart, keep them on the same page
        return redirect(request.META.get("HTTP_REFERER", "main"))


    else:   
        return redirect("main")


def view_cart(request):
    cart = request.session.get("cart", {})

    # debugging 
    print("DEBUG: View Cart Function - Retrieved session data:")
    print(cart)

    # initiate the total count
    total = 0
    
    # access each product in cart consideing it is a dictionary 
    for id, data in cart.items():

        # calculate total
        sub_total = float(data['price']) * int(data['qty'])

        # add together the subtotal
        total += sub_total
    
    return render(request, "view_cart.html", {
        "cart": cart,
        "total": total,
    })

def edee_farms(request):
    return render(request, "edee_farms.html")

@ratelimit(key='ip', rate='3/m', block=True)
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

@ratelimit(key='ip', rate='5/m', block=True)
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
    cheapest = Price.objects.values('foodstuff').annotate(min_price=Min('price')).order_by('min_price')[:5]
    expensive = Price.objects.values('foodstuff').annotate(max_price=Max('price')).order_by('-max_price')[:5]

    # Logic for "Regional Comparison"
    lowest_records = (
        Price.objects.values('foodstuff')
        .annotate(min_price=Min('price'))
    )

    regional_comparison = []
    for record in lowest_records:
        foodstuff = record['foodstuff']
        min_price = record['min_price']

        lowest_entry = (
            Price.objects.filter(foodstuff=foodstuff, price=min_price)
            .order_by('created_at')
            .first()
        )

        if lowest_entry:
            regional_comparison.append({
                'foodstuff': foodstuff,
                'market': lowest_entry.market_store_name[:15],
                'state': lowest_entry.state,
                'price': lowest_entry.price,
            })

    random.shuffle(regional_comparison)
    regional_comparison = regional_comparison[:5]


    # Logic for "Price Trends"
    today = datetime.date.today()
    this_week_start = today - datetime.timedelta(days=7)
    last_week_start = today - datetime.timedelta(days=14)
    items = ["Rice (local)", "Rice (foreign)", "Beans (brown)", "Beans (white)", "Yam", "Garri (white)", "Garri (yellow)", "Maize"]
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
            status = "Not available."
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
        'regional_comparison': regional_comparison,
    })

def states_listing(request, state):
    prices = Price.objects.filter(state=state) #states like Akwa Ibom and Cross River now appear as expected
    return render(request, 'state_listing.html', {
        'state': state,
        'prices': prices
    })

# These views relate to the AI chatbot section

# Set up a logger for debugging
logger = logging.getLogger(__name__)

# Geopy geolocator instance
# Note: Set a unique user_agent to comply with Nominatim's usage policy.
geolocator = Nominatim(user_agent="Main")

def _handle_db_query(user_input):
    """Handles requests to query the database."""
    # Create an OpenAI client instance for each request
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    sql_prompt = """
Translate the following natural language query into a JSON object with keys:
- "model": The Django model name.
- "filters": A dictionary of key-value pairs for filtering.
- "order_by": The field to order by.
- "limit": An integer for the number of results.

Query: "Show me the top 5 most expensive foodstuffs in Abuja."
Expected JSON: '{"model": "Price", "filters": {"lga": "Abuja"}, "order_by": "-price", "limit": 5}'

Query: "What's the price of a bag of rice in Lugbe?"
Expected JSON: '{"model": "Price", "filters": {"foodstuff": "bag of rice", "lga": "Lugbe"}, "order_by": "", "limit": 1}'

Query: "List all prices in Wuse 2."
Expected JSON: '{"model": "Price", "filters": {"lga": "Wuse 2"}, "order_by": "", "limit": 0}'

Query: "{user_input}"
Expected JSON:
"""
    try:
        # Use the new chat completions endpoint
        completion_sql = client.chat.completions.create(
            model="gpt-3.5-turbo", # Use a modern chat-optimized model
            messages=[
                {"role": "user", "content": sql_prompt.format(user_input=user_input)}
            ]
        )
        
        # Access the content from the new response format
        raw_response = completion_sql.choices[0].message.content
        
        query_plan = json.loads(raw_response.strip() + '}')

        if query_plan.get('model') != 'Price':
            return JsonResponse({'reply': "I can only query the Price model."})
        
        queryset = Price.objects.all()
        filters = query_plan.get('filters', {})
        if filters:
            queryset = queryset.filter(**filters)
        
        order_by = query_plan.get('order_by', '')
        if order_by:
            queryset = queryset.order_by(order_by)
        
        limit = query_plan.get('limit', 0)
        if limit > 0:
            queryset = queryset[:limit]
        
        results = list(queryset.values())
        
        if not results:
             return JsonResponse({'reply': "I couldn't find any data matching your request."})

        # Translate results to natural language
        nl_prompt = f"The following data was retrieved from a database: {results}. Please rephrase this into a concise, natural language response for a user."
        
        completion_nl = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": nl_prompt}
            ]
        )
        
        final_reply = completion_nl.choices[0].message.content
        
        return JsonResponse({'reply': final_reply})

    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'reply': "I'm sorry, I couldn't understand that query. Can you try rephrasing it?"})
    except Exception as e:
        logger.error(f"Database query error: {e}")
        return JsonResponse({'reply': f"An error occurred while fetching data: {str(e)}"})


def _handle_distance_query(user_input):
    """Handles requests to calculate distance between locations."""
    # Create an OpenAI client instance for each request
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    location_prompt = f"""
Extract two locations from the following query in a JSON object with keys 'location1' and 'location2'.

Query: "How far is Gwarinpa, Abuja from Nyanya Market?"
Expected JSON: '{{ "location1": "Gwarinpa, Abuja", "location2": "Nyanya Market" }}'

Query: "{user_input}"
Expected JSON:
"""
    try:
        # Use the new chat completions endpoint
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": location_prompt.format(user_input=user_input)}
            ]
        )
        
        raw_response = completion.choices[0].message.content
        
        locations = json.loads(raw_response.strip() + '}')
        loc1_name = locations.get('location1')
        loc2_name = locations.get('location2')

        if not loc1_name or not loc2_name:
            return JsonResponse({'reply': "I couldn't identify both locations. Please try again."})
        
        loc1_coords = geolocator.geocode(loc1_name).point
        loc2_coords = geolocator.geocode(loc2_name).point
        
        distance = geodesic(loc1_coords, loc2_coords).km
        
        final_prompt = f"The distance between {loc1_name} and {loc2_name} is {distance:.2f} kilometers. Rephrase this as a simple, natural language sentence."
        
        final_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": final_prompt}
            ]
        )
        
        final_reply = final_completion.choices[0].message.content
        
        return JsonResponse({'reply': final_reply})
        
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'reply': "I couldn't find coordinates for one of the locations. Please check the spelling."})
    except Exception as e:
        logger.error(f"Distance query error: {e}")
        return JsonResponse({'reply': f"An error occurred while calculating the distance: {str(e)}"})


def _handle_general_chat(user_input):
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for foodstuff prices and local markets in Abuja, Nigeria. Keep your responses concise and friendly."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        return JsonResponse({'reply': completion.choices[0].message.content.strip()})
    except Exception as e:
        logger.error(f"General chat error: {e}")
        return JsonResponse({'reply': f"An error occurred: {str(e)}"})

def chatbot(request):
    """Main view to handle all chatbot requests by classifying intent."""
    if request.method == 'GET':
        return render(request, 'chat_interface.html')

    elif request.method == 'POST':
        try:
            # Create an OpenAI client instance for the main view
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

            data = json.loads(request.body)
            user_input = data.get('input', '')

            if not user_input:
                return JsonResponse({'reply': 'Please enter a message.'})

            # --- Intent Classification: The brain of the operation ---
            intent_prompt = f"""
Classify the following user request into one of these categories:
- 'query_db' (if the user asks about prices, markets, or foodstuffs)
- 'calculate_distance' (if the user asks for the distance between two locations)
- 'general_chat' (for all other questions, like greetings or general inquiries)

User Request: "How far is Gwarinpa from Nyanya market?"
Category: calculate_distance

User Request: "What is the price of tomatoes in Wuse?"
Category: query_db

User Request: "hello, how are you?"
Category: general_chat

User Request: "{user_input}"
Category:"""

            # Use the new chat completions endpoint for classification
            intent_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": intent_prompt.format(user_input=user_input)}
                ],
                max_tokens=20,
                stop=['\n']
            )
            
            intent = intent_completion.choices[0].message.content.strip()

            # --- Route the request based on intent ---
            if intent == 'query_db':
                return _handle_db_query(user_input)
            elif intent == 'calculate_distance':
                return _handle_distance_query(user_input)
            else:
                return _handle_general_chat(user_input)

        except Exception as e:
            # Removed the duplicate client creation and moved it to the top
            logger.error(f"Main view error: {e}")
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)