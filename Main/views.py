from django.http import HttpResponse
from django.template import loader
from .models import Memebers

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
