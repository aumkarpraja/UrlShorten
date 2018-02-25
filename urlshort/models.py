from django.db import models

# Create your models here.
class Urls(models.Model):
    short_id = models.SlugField(primary_key = True, max_length=6) # shortened ID of the URL
    given_URL = models.URLField(max_length=350) # the URL (long version) given by user
    published_date = models.DateTimeField(auto_now=True) # Date of shortening
    count = models.IntegerField(default=0) # Number of times this specific URL was visited
    client_ip = models.GenericIPAddressField(protocol='both',default="0.0.0.0") # IP of user who submitted link
def __str__(self):
    return self.given_URL