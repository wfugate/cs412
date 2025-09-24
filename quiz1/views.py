from django.shortcuts import render

# Create your views here.

def main_page(request):
    template_name = 'quiz1/main.html'
    print()
    return render(request, template_name)


def submit_page(request):
    template_name = 'quiz1/display.html'

    favorite_ice_cream = request.POST.get("ice_cream", 'no ice cream provided')
    
    context = {
        "ice_cream" : favorite_ice_cream
    }
    return render(request, template_name, context)
        
    

