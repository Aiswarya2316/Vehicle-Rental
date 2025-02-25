from django.shortcuts import render



def home(request):
    return render(request,'home.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import now




# Customer Registration
def customer_register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer registered successfully!")
            return redirect("login")
    else:
        form = CustomerRegistrationForm()
    return render(request, "customer/register.html", {"form": form, "user_type": "Customer"})



# Seller Registration
def staf_register(request):
    if request.method == "POST":
        form = StafRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seller registered successfully!")
            return redirect("login")
    else:
        form = StafRegistrationForm()
    return render(request, "staf/register.html", {"form": form, "user_type": "Seller"})



# Admin Registration
def admin_register(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin registered successfully!")
            return redirect("login")
    else:
        form = AdminRegistrationForm()
    return render(request, "admin/register.html", {"form": form, "user_type": "Admin"})



# --- User Login ---
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = None
            redirect_url = "login"  # Default in case of failure

            if Customer.objects.filter(email=email, password=password).exists():
                user = Customer.objects.get(email=email)
                request.session["user_type"] = "Customer"
                redirect_url = "customerhome"
            elif Staf.objects.filter(email=email, password=password).exists():
                user = Staf.objects.get(email=email)
                request.session["user_type"] = "Staf"
                redirect_url = "stafhome"
            elif AdminReg.objects.filter(email=email, password=password).exists():
                user = AdminReg.objects.get(email=email)
                request.session["user_type"] = "Admin"
                redirect_url = "adminhome"

            if user:
                request.session["user_id"] = user.id
                messages.success(request, f"Welcome {user.name}!")
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid credentials")

    form = LoginForm()
    return render(request, "login.html", {"form": form})



# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")




def adminhome(request):
    return render(request,'admin/adminhome.html')



def stafhome(request):
    return render(request,'staf/stafhome.html')



def customerhome(request):
    return render(request,'customer/customerhome.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle, Staf
from .forms import VehicleForm

# Add Vehicle
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully!")
            return redirect("vehicle_list")
        else:
            messages.error(request, "Error adding vehicle. Please check the details.")
    else:
        form = VehicleForm()

    staff_list = Staf.objects.all()
    return render(request, "staf/add_vehicle.html", {"form": form, "staff_list": staff_list})

# View Vehicles
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "staf/vehicle_list.html", {"vehicles": vehicles})

# Update Vehicle
def update_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully!")
            return redirect("vehicle_list")
        else:
            messages.error(request, "Error updating vehicle. Please check the details.")
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, "staf/update_vehicle.html", {"form": form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle, Booking
from datetime import date

def vehicle_lists(request):
    """ Display all available vehicles """
    vehicles = Vehicle.objects.filter(availability=True)
    return render(request, "customer/vehicle_list.html", {"vehicles": vehicles})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle, Booking
from datetime import date

def book_vehicle(request, vehicle_id):
    """Handle vehicle booking without authentication"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        customer_name = request.POST.get("customer_name")
        customer_phone = request.POST.get("customer_phone")

        if not (start_date and end_date and customer_name and customer_phone):
            messages.error(request, "All fields are required.")
            return redirect("book_vehicle", vehicle_id=vehicle.id)

        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        if start_date >= end_date:
            messages.error(request, "End date must be after the start date.")
            return redirect("book_vehicle", vehicle_id=vehicle.id)

        # Create the booking
        booking = Booking.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date
        )

        # Mark vehicle as unavailable
        vehicle.availability = False
        vehicle.save()

        messages.success(request, "Vehicle booked successfully!")
        return redirect("vehicle_lists")

    return render(request, "customer/book_vehicle.html", {"vehicle": vehicle})






from django.shortcuts import render
from .models import Booking

def booking_history(request):
    """Display all bookings with updated status"""
    bookings = Booking.objects.all().order_by("-id")  # Fetch latest bookings first
    return render(request, "customer/booking_history.html", {"bookings": bookings})



import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Booking

def make_payment(request, booking_id):
    """Initiate Razorpay payment"""
    booking = get_object_or_404(Booking, id=booking_id)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create an order in Razorpay
    order_data = {
        "amount": int(booking.total_price * 100),  # Amount in paisa
        "currency": "INR",
        "payment_capture": "1",
    }
    order = client.order.create(data=order_data)

    return render(
        request,
        "customer/payment.html",
        {
            "booking": booking,
            "order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID
        },
    )





from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
import json

@csrf_exempt
def payment_success(request):
    """Update booking payment status on successful payment"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")
            payment_id = data.get("razorpay_payment_id")

            if not booking_id or not payment_id:
                return JsonResponse({"status": "error", "message": "Invalid payment data"}, status=400)

            # Get the booking and update the payment status
            booking = get_object_or_404(Booking, id=booking_id)
            booking.payment_status = "Paid"
            booking.save(update_fields=["payment_status"])

            messages.success(request, "Payment successful! Your booking is confirmed.")
            return JsonResponse({"status": "success", "message": "Payment successful!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid data received"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)





def about (request):
    return render(request,'customer/about.html')