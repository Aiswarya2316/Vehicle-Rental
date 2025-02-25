from django.contrib import admin
from .models import Customer, Staf, AdminReg, Vehicle, Booking

# Register all models
admin.site.register(Customer)
admin.site.register(Staf)
admin.site.register(AdminReg)
admin.site.register(Vehicle)
admin.site.register(Booking)
