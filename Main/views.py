from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Memebers
from .forms import ContactForm
from django.shortcuts import redirect
from django.contrib import auth

# Create your views here.
def members(request):
    mymembers = Memebers.objects.all().values()
    template = loader.get_template('myfirst.html')
    context = {
    'mymembers' : mymembers,
    }

    return HttpResponse(template.render(context, request))

def details(request, id):
    memberid = Memebers.objects.get(id=id) 
    template = loader.get_template('details.html')
    context = {
        'memberid': memberid
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    context = {
        'main' : main,
    }
    return HttpResponse(template.render(context, request))

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            send_mail (
                'Feedback from your site, topic: %s' % topic,
                message, 
                sender,
                ['investor@gmail.com']
            )
            return redirect('main')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form':form})    

def search_view(request):
    query=request.GET.get('q', '')
    results = []
    if query:
        results = Memebers.objects.filter(shopname_icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

# def contact(request):
    template = loader.get_template('contact.html')
    context = {
        'forms': form,
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
