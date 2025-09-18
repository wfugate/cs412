### restaurant/views.py
### controls the views for the restaurant app
### Author: William Fugate
from django.shortcuts import render
import random
from datetime import datetime, timedelta

#list of daily specials to choose randomly from
specials = ["Chicken Sandwich", "Philly Cheese Steak", "Veggie Burger", "Fish Sandwich"]

#menu items with prices for calculating total
menu_prices = {
    "Hamburger": 8.99,
    "Cheeseburger": 9.99,
    "Fries": 3.99,
    "Curly Fries": 4.99,
    "Add veggies": 1.00,
    "special": 10.99
}

def main(request):
    '''Main view for the main page'''
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    '''View for the ordering page with daily special'''
    template_name = 'restaurant/order.html'
    
    context = {
        "special": random.choice(specials) #choose a random special each time the page loads
    }
    return render(request, template_name, context)

def confirmation(request):
    '''Process form submission and display confirmation page'''
    template_name = 'restaurant/confirmation.html'
    
    if request.method == 'POST': #get user data from form submission
        name = request.POST.get("name", "No Name Provided")
        email = request.POST.get("email", "No Email Provided")
        phone = request.POST.get("phone", "No Phone Provided")
        
        #tracking variables for ordered items and total price
        ordered_items = []
        total_price = 0.0
        
        #checking each item to see if it was ordered
        for item_name, price in menu_prices.items():
            if request.POST.get(item_name):
                if item_name == "special":
                    #get the actual special name from the checkbox value
                    special_name = request.POST.get("special")
                    ordered_items.append(f"{special_name} (Daily Special)")
                else:
                    ordered_items.append(item_name)
                total_price += price

        instructions = request.POST.get("special_instructions", "").strip() #getting special instructions if any

        #calculate random ready time
        current_time = datetime.now()
        random_minutes = random.randint(30, 60)
        ready_time = current_time + timedelta(minutes=random_minutes)
        ready_time_formatted = ready_time.strftime("%I:%M %p")
        
        context = {
            "name": name,
            "email": email,
            "phone": phone,
            "ordered_items": ordered_items,
            "total_price": total_price,
            "ready_time": ready_time_formatted,
            "instructions": instructions
        }
    return render(request, template_name, context)