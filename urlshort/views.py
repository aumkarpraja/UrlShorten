from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from urlshort.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from ipware import get_client_ip

import string, json, random, re


# Create your views here.
def index(request):
    return render(request, 'index.html')

def statsindex(request):
    return render(request, 'stats.html')

# This would happen if the user is trying to get to the original page via shortened URL
def redirect(request, short_id):
    # Try to find the URL, if not, get_object_or_404
    url = get_object_or_404(Urls, pk=short_id)
    url.count += 1 # it's been accessed so iterate it's count
    url.save() # save stats
    # Send it off to the page requested
    return HttpResponseRedirect(url.given_URL)

def shorten(request):
    # Get the filled out URL via POST
    url = request.POST.get("url")
    # Check to make sure something is there to shorten
    if not (url == ''):
        # Add on http to the start of the text if the user opted not to add it
        if not(re.search("http://", url)):
            url = "http://" + url
        short_id = short_id_gen() #run the generator
        
        # Get user IP
        user_ip = get_client_ip(request)

        # Add to db
        b = Urls(given_URL = url, short_id = short_id, client_ip = user_ip[0])
        b.save() # save to db

        # We need to provide a response of some type after it's shortened, obviously
        # we want to give the user back a shortened URL so...
        response_data = {}
        output = "https://aumkar-urlshorten.herokuapp.com" + "/" + short_id # putting together the shortened URL
        return render(request, 'index.html', {'output':output })
    # If we've reached this return state, obviously the URL was incorrect or something else is going on our end
    return render(request, 'index.html', {'output':"Some error occured." })

def get_stats(request):
    url = request.POST.get("url")
    short_id = url[-6:] #slice last 6 characters, those SHOULD be the short_id if formed properly
    try:
        # Get all output details (from DB)
        output = Urls.objects.get(pk=short_id)
        output_count = output.count
        output_url = output.given_URL
        output_ip = output.client_ip
        pub_date = output.published_date
        return render(request, 'stats.html', {'outputCount': "Link click count: " + str(output_count), 'outputURL': "Link original URL: " +output_url, 'requestIP': "Submit IP: " + str(output_ip), 'pubDate': "Published date: " + str(pub_date)})
    except:
        return render(request, 'stats.html', {'outputCount':"Link not found."})
# This is the "algo" that shortens the URL using a series of random characters, digits
def short_id_gen():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if id used, find another one
    while True:
        short_id = ''.join(random.choice(char) for i in range(length))
        try:
            tmp = Urls.objects.get(pk=short_id) 
        except:
            return short_id
  