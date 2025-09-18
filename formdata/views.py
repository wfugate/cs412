from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
def show_form(request):
    '''Respond to the URL 'show_form', delegate work to a template'''

    template_name = 'formdata/form.html'


    return render(request, template_name)

def submit(request):
    '''Process the form submission, and generate a result.'''

    if request.POST:
        name = request.POST.get("name", "No Name Provided")
        favorite_color = request.POST.get("favorite_color", "No Color Provided")
        context = {
            "name": name,
            "favorite_color": favorite_color,
        }
    return render(request, 'formdata/confirmation.html', context)