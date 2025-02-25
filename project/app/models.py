from django.db import models
from datetime import date, timedelta

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Staf(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AdminReg(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    staf = models.ForeignKey(Staf, on_delete=models.CASCADE, related_name="vehicles")  # Assign vehicles to Staf
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to="vehicle_images/", blank=True, null=True)  # Optional Image

    def __str__(self):
        return f"{self.name} - {self.model}"
    
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        rental_days = (self.end_date - self.start_date).days
        self.total_price = self.vehicle.price_per_day * rental_days  # Calculate total price
        super().save(*args, **kwargs)

    def extend_rental(self, extra_days):
        """ Extend the rental period and update price """
        self.end_date += timedelta(days=extra_days)
        self.save()

    def __str__(self):
        return f"{self.customer.name} booked {self.vehicle.name} from {self.start_date} to {self.end_date}"
