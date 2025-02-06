from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
import uuid

# Create your models here.

class User(AbstractUser):
    
     is_verified = models.BooleanField(default=False)

     otp = models.CharField(max_length=6,null=True,blank=True)
    
     phone = models.CharField(max_length=12,null=True)

     def generate_otp(self):
        
        self.otp = str(randint(100000,999990)) + str(self.id)

        self.save()
        
class BaseModel(models.Model):
    
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Hotel(BaseModel): 
    hotel_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    
    address = models.TextField(max_length=100, null=True)
    description = models.TextField(null=True)
    rating = models.FloatField(default=0)

    
    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
    ]
    
    TYPE = [
        ("king", "King"),
        ("queen", "Queen"),
        ("double", "Double"),
        ("single", "Single"),
    ]  
    image = models.ImageField(upload_to="hotel_images", null=True)
    room_type = models.CharField(choices=TYPE ,default="king",max_length=50, null=True)
    is_booked = models.BooleanField(default=False)
    room_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available")
    price = models.PositiveIntegerField(null=True)
    Amenity = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f"{self.hotel_name} - {self.location}"
    

class Booking(BaseModel):
    
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings",)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateTimeField()
    location = models.CharField(max_length=50,null=True)
    checkout = models.DateTimeField()
    persons = models.PositiveIntegerField()
    is_confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False) 
    
    # payment = [
    #     ("online","online"),
    #     ("prepaid","prepaid"),
    # ]
    # payment_method = models.CharField(max_length=50,choices=payment,default="online",null=True)
    # rzp_id = models.CharField(max_length=100,null=True)
     
      
    
    
    def __str__(self):
        return f"{self.customer.username} booked {self.hotel.hotel_name} - {self.hotel.room_type}"
    
