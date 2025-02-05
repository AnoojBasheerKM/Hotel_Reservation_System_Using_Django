from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.views.generic import View
from hotel.models import User,Hotel,Booking
from hotel.forms import UserForm,LoginForm,BookingForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.

class UserRegistrationView(View):
    
    template_name = "registration.html"
    
    form_class = UserForm
    
    def get(self,request,*args,**kwargs):
        
        forms = self.form_class()
        
        return render(request, self.template_name,{"form":forms})
    
    def post(self,request,*args,**kwargs):
        
        form_data = request.POST
        
        form_instance = self.form_class(form_data)
        
        print (form_data)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect('signin')
            
        return render(request, self.template_name,{"form":form_instance})
    
class UserSignInView(View):
    
    template = "login.html"
    
    form_class = LoginForm
    
    def get(self,request,*args,**kwargs):
        
        form = self.form_class()
        
        return render(request,self.template,{"form":form})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            uname = form.cleaned_data.get('username')

            pwd = form.cleaned_data.get('password')
            
            user_obj = authenticate(request,username = uname,password = pwd)
            
            if user_obj:
                
                login(request,user_obj)
                
                return redirect('home')

                
        return render(request, self.template, {"form": form})
    
class UserSignoutView(View):
    
    def get(self,request,*args,**kwargs):
        
        logout(request)
        
        return redirect('signin')
    
        
        
    
class Home(View):
    
    template_name = "index.html"
    
    def get(self,request,*args,**kwargs):
        
        return render(request, self.template_name)


    
class HotelView(View):
    
    template_name = "hotel_list.html"
    
    def get(self,request,*args,**kwargs):
        
        location = request.GET.get("location")
        
        print(location)
        
        hotels = Hotel.objects.filter(location=location) if location else Hotel.objects.all()
        
        return render(request, self.template_name,{"hotels":hotels,"location":location})

class BookingView(View):
    
    template_name = "booking.html"
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get("uid")
        
        hotel = get_object_or_404(Hotel,uid = id)
        
        form = BookingForm(initial={"hotel":hotel.hotel_name,"location":hotel.location})
        
        return render(request, self.template_name,{"form":form,"hotel":hotel})
    
    def post(self,request,*args,**kwargs):
        
        id = kwargs.get("uid")
        
        hotel = get_object_or_404(Hotel,uid=id)
        
        form = BookingForm(request.POST)

        if form.is_valid():
            
            if form.is_valid():
                
                booking = form.save(commit=False)
                
                booking.customer = request.user
                
                booking.is_confirmed = True 
               
                booking.is_paid = False
                
                booking.save()
                
                return   HttpResponse("booking is successfull")
            
            return render(request, self.template_name, {"form": form, "hotel": hotel})
        

        
        
        