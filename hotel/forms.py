from django import forms
from hotel.models import User,Booking
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',"phone"]
        widgets = {"username": forms.TextInput(attrs={'class': 'form-control','placeholder':' Enter Username'}),
                     "email": forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter Your Email'}),
                     "phone": forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Phone number'}),
                     "password1": forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password1'}),
                     "password2": forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password2'}),
        }
        
class LoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})) 

class BookingForm(forms.ModelForm):
    
    class Meta:
    
        model = Booking
    
        fields = ["hotel","location","check_in","checkout","persons"]
    
        widgets = {
        
            "hotel": forms.TextInput(attrs={'class': 'form-control'}),
            "check_in": forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            "checkout": forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            "persons": forms.NumberInput(attrs={'class': 'form-control'}),
            "location": forms.TextInput(attrs={'class': 'form-control'})
        }
        
        