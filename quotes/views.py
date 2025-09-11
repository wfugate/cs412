# File: views.py
# Author: William Fugate wfugate@bu.edu
# Description: the view controller for a quotes application
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

#list of images of Del Water Gap
images = ["https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/DWGNYC2020_%28cropped%29.jpg/960px-DWGNYC2020_%28cropped%29.jpg", "https://mp-admin.tps-dev.co.uk/wp-content/uploads/2023/09/MAINDelWaterGapAWEDIT1creditEricaSnydercopy.jpg", "https://cdn.grove.wgbh.org/7c/9d/a23817c1a1ec2654123eb1860e02/img-3718.jpg", "https://imgix.bustle.com/uploads/image/2023/9/21/31bf58cb-af97-4008-8b2a-c539e46e9b37-new-faces_-delwatergap.jpg?w=414&h=518&fit=crop&crop=focalpoint&dpr=2&fp-x=0.423&fp-y=0.2635"]
#list of quotes from Del Water Gap
quotes = ["Therapy. Please y'all, call a therapist", "Call me Midas in reverse, ’cause everything I touch turns eventually to dirt.", "When we’re struggling—whether with anxiety, loneliness, or addiction—often we get this horrible solipsistic feeling, like, ‘No one else could possibly feel this bad.’ A lot of my recent work has come from that feeling, and it has been very cathartic to see it resonate with a lot of other people. It’s absolutely cathartic; it’s therapy that results from therapy. I’ll see my therapist, then I’ll go home and write a song.", "The magic is when a song stops being mine and starts belonging to everyone in the room."]


def quote_page(request):
    '''Respond to the URL 'quote', delegate work to a template'''

    template_name = 'quotes/quote_page.html'

    context = {
        "displayQuote": quotes[random.randint(0,3)], #select a quote at random
        "displayImage": images[random.randint(0,3)], #select an image at random
    }

    return render(request, template_name, context)

def show_all_page(request):
    '''Respond to the URL 'show_all', delegate work to a template'''

    template_name = 'quotes/show_all_page.html'

    context = {
        "images": images,
        "quotes": quotes,
    }

    return render(request, template_name, context)

def about_page(request):
    '''Respond to the URL 'about_page', delegate work to a template'''

    template_name = 'quotes/about_page.html'


    return render(request, template_name)