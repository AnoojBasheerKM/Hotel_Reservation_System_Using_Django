
from django.urls import path
from hotel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',views.UserRegistrationView.as_view(),name='signup'),
    path('signin/',views.UserSignInView.as_view(),name="signin"),
    path('signout/',views.UserSignoutView.as_view(),name='logout'),
    path('home/',views.Home.as_view(), name='home'),
    path('hotels/',views.HotelView.as_view(), name='hotel_list'),
    path('booking/<uuid:uid>/',views.BookingView.as_view(), name='booking'),
   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)