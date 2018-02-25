from django.conf.urls import include, url 

import urlshort.views

urlpatterns = [
    # The main page
    url(r'^$', urlshort.views.index, name='index'),

    # Redirect when short url is requested to original URL
    url(r'^(?P<short_id>\w{6})$', urlshort.views.redirect, name='redirect1'),

    # Shortens the URL
    url(r'^shorten/', urlshort.views.shorten, name='shorten'),
]