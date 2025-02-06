from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.views.generic import View
from hotel.models import User,Hotel,Booking
from hotel.forms import UserForm,LoginForm,BookingForm
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from hotel.decorators import signin_required
from django.views.decorators.cache import never_cache
# Create your views here.

decs=[signin_required,never_cache]


# def send_otp_email(user):
    
#     user.generate_otp()

#     subject = "verify your email"

#     message = f"otp for account verification is {user.otp} otp valid for only 10 minutes "

#     from_email = ('')

#     to_email = [user.email]
    
#     send_mail(subject,message,from_email,to_email)

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
  
@method_decorator(decs,name="dispatch")  
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
    
@method_decorator(decs,name="dispatch")
class BookingView(View):
    
    template_name = "booking.html"
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get("uid")
        
        hotel = get_object_or_404(Hotel,uid = id)
        
        form = BookingForm(initial={"hotel":hotel.uid,"hotel_name":hotel.hotel_name,"location":hotel.location})
        
        return render(request, self.template_name,{"form":form,"hotel":hotel})
    
    def post(self,request,*args,**kwargs):
        
        id = kwargs.get("uid")
        
        hotel = get_object_or_404(Hotel,uid=id)
        
        data = request.POST
        
        form = BookingForm(data)
        
        # print(id)
        
        # print(data)

            
        if form.is_valid():
            
           
                
            booking = form.save(commit=False)
            
            booking.hotel = hotel
                
            booking.customer = request.user
                
            booking.is_confirmed = True 
               
            booking.is_paid = False
                
            booking.save()
            
            hotel.is_booked = True
            
            hotel.room_status = "booked"
            
            hotel.save()
            
            print("validation success")
                
            return redirect('booking_list')
        
        print("validation failed")
           
        return render(request, self.template_name, {"form": form, "hotel": hotel})
    
@method_decorator(decs,name="dispatch")
class UserBookingListView(View):
     
     template = 'Your_bookings.html'
     
     def get(self,request,*args,**kwargs):
         
         bookings = Booking.objects.filter(customer=request.user)
         
         return render(request,self.template,{"bookings":bookings})
     
@method_decorator(decs,name="dispatch")     
class CancelBookingView(View):
    
    def post(self,request,*args,**kwargs):
        
        id = kwargs.get("uid")
        
        booking = get_object_or_404(Booking, customer=request.user, uid=id)
        
        booking.is_confirmed = False
        
        booking.save()
        
        booking.delete()
        
        print("booking cancelled and deleted")
        
        
        return redirect('booking_list')
        

        
        
        