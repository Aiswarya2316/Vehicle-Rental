from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('stafhome',views.stafhome,name='stafhome'),
    path('customerhome',views.customerhome,name='customerhome'),
    path("registercustomer/", views.customer_register, name="customer_register"),
    path("registerstaf/", views.staf_register, name="seller_register"),
    path("registeradmin/", views.admin_register, name="admin_register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("addvehicle/",views.add_vehicle,name='add_vehicle'),
    path("vehiclelist/",views.vehicle_list,name='vehicle_list'),
    path("updatevehicle/<int:vehicle_id>/",views.update_vehicle,name='update_vehicle'),
    path("vehiclelists/",views.vehicle_lists,name='vehicle_lists'),
    path("book/<int:vehicle_id>/", views.book_vehicle, name="book_vehicle"),
    path("booking-history/", views.booking_history, name="booking_history"),
    path("make-payment/<int:booking_id>/", views.make_payment, name="make_payment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("about/", views.about, name="about"),



    
]
