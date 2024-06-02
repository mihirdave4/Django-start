from django.contrib import admin
from django.urls import path,include
from myapp1 import views
from django.conf import settings
from django.conf.urls.static import static
from myapp1.views import userdetail,Verify_otp
from .views import RegiserAPI
from django.contrib.auth import views as auth_views




urlpatterns = [

   path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
   path('logout/',auth_views.LogoutView.as_view()),
   path('',views.eventdash,name='home'),
   path('verify/',Verify_otp.as_view()),
    path('book/<int:id>',views.details, name="booktick"),
   path('userdetail/',views.userdetail,name="userdetail"),
   path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
   path('redirect/',views.success,name='success'),
     path('payment/', views.homepage, name='index'),
    path('payment/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('done/',views.paymentdone,name="paymentdone"),
    path('payment/invoices/',views.invoices,name='invoices'),
    path('invoice/',views.invoice,name='invc'),
    path('/contactus/',views.contactus,name='contactus'),
path('regis/',RegiserAPI.as_view()),
   # path('eventdash/eventdash/book/invoice/',views.invoices, name="invoices"),
   path('eventdash/',views.eventdash),
   # path('my_button/', views.razorbook, name='my_button_url'),
   
   
  

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)