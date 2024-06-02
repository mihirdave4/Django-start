import base64
import io
from django.shortcuts import render,HttpResponse
from .models import event, location,Ticket,userqr2,Clients
from django.http import HttpResponseBadRequest
from django.conf import settings
import requests.sessions,requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import smtplib
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.shortcuts import redirect
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import random
import qrcode
import datetime
from django.core.mail import EmailMessage
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from .serializer import UserSerializer,VerifyAccountSerializer
# Create your views here.
from mysite.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
from .emails import *
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.urls import reverse


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# def homepage(request):
        
#     if request.method == "POST":
#         name= request.POST.get('name')
#         mobile= request.POST.get('mobile')
#         email= request.POST.get('email')

        

#         currency = 'INR'
#         amount = 20000 # Rs. 200

#         # Create a Razorpay Order
#         razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                         currency=currency,
#                                                         payment_capture='0'))

#         # order id of newly created order.
#         razorpay_order_id = razorpay_order['id']
#         callback_url = 'paymenthandler/'

#         # we need to pass these details to frontend.
#         context = {}
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         context['razorpay_amount'] = amount
#         context['currency'] = currency
#         context['callback_url'] = callback_url

#         return render(request, 'done.html', context=context)
#     else:
#          print("---------------------------------------------------")


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'done.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'done.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()

def paymentdone(request):
     return render(request,'done.html')


def send_otp_email(request, email):
    otp = str(random.randint(1000, 9999))  # Generate a random OTP
    message = f'Your OTP: {otp}'
    send_mail('OTP Verification', message, 'your-email@example.com', [email])
    return otp



class RegiserAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'Registration successful, check email',
                    'data': serializer.data,
                })
            else:
                return Response({
                    'status': 400,
                    'message': 'Something went wrong',
                    'data': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               


class Verify_otp(APIView):
     def post(self,request):
        try:
            data= request.data
            serializer= VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email =serializer.data['email']
                otp= serializer.data['otp']

                user= User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'User with given email does not exit',
                        'data': 'invalid email',
                    }, status=status.HTTP_400_BAD_REQUEST)

                elif user.exists():
                    # main_user=User.objects.get(email=email)
                    if  user[0].otp== otp:
                        user= user.first()
                        user.is_verified=True
                        user.save()
                        return Response({
                            'status': 200,
                            'message': 'Validation has been successfull',
                            'data': serializer.data,
                        })

                    else:
                        return Response({
                            'status':400,
                            'message':f'Enter valid otp sent to your email id {email}',
                            'data':'Wrong otp'
                        })
            else:

                return Response({
                    'status': 400,
                    'message': 'Something went wrong',
                    'data': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               



from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Payorderss2
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 

 
def homepage(request):
    tp= request.session.get('total_price')

    if request.method == "POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        mobile= request.POST.get('mobile')
        eventid= request.POST.get('eventid')
        request.session['name'] = name
        request.session['email'] = email
        request.session['mobile'] = mobile
        currency = 'INR'
        amount = tp*100  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        

    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        request.session['razor_order_id']= razorpay_order_id
        callback_url = f'paymenthandler/?name={name}&email={email}&mobile={mobile}'
        # order = Payorderss1.objects.create(name=name,
        #                              id=razorpay_order_id,
        #                              number=mobile,
        #                              email=email,
        #                              tickettype= 'Gold',
        #                              number_of_tickets= 4,


        #                             #  orderid= razorpay_order_id ,
        #                             #  number_of_tickets=1)
        #                             )


# Create a new Payorderss1 object and assign the event object to the eventid field
        tp= request.session.get('total_price')
        number_ticket= request.session.get('number_ticket')
        event_id= request.session.get('event_id')
        event_name= request.session.get('event_name')
        event_obj = event.objects.get(pk=event_id)
        tickettype= request.session['ticket_type_real']
        order = Payorderss2(name=name, email=email, number=mobile, id=razorpay_order_id, eventid=event_obj,totalprice=tp,number_of_tickets= number_ticket,tickettype=tickettype)
        order.save()
        request.session['order_id'] = order.id
        # we need to pass these details to frontend.
        context = {}
        context['name']= name
        context['email']= email
        context['mobile']= mobile
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['eventid']= eventid
        context['currency'] = currency
        context['callback_url'] = callback_url


        return render(request, 'index.html', context=context)



 
 

def home(request):
    return render('eventdash.html')




@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'invoices.html',razorpay_order_id)
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
 




from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

class GeneratePdf(View):
    # name = request.session.get('name')
    # email = request.session.get('email')
    # mobile = request.session.get('mobile')
    def get(self, request, *args, **kwargs):
        template = get_template('pdf_template.html')
        context = {
            'val1': kwargs['val1'], #passing val1 as a context variable
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_file.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response








def invoices(request):
    import datetime

    now = datetime.datetime.now()

    name = request.session.get('name')
    email = request.session.get('email')
    mobile = request.session.get('mobile')
    request.session['user_name']="mihir"
    tp= request.session.get('total_price')
    loc= request.session.get('loc')
    event_name= request.session.get('event_name')
    event_id= request.session.get('event_id')
    order_id= request.session.get('razor_order_id')
    even = list(event.objects.filter(eventid=event_id).values())
    tickettype= request.session.get('tickettype')
    # tickettype = request.session.get('tickettype')
    # ticket_type = tickettype.type_of_ticket
    number_ticket= request.session.get('number_ticket')
    ticket_type= request.session['ticket_type_real']
    ticket_price1= request.session.get('ticket_price1')
    # ticket_price= request.session['ticket_price']
    even1 = event.objects.get(eventid=event_id)

# get the image and read the binary data
    image_binary = even1.image.read()

    # encode the binary data to base64
    image_base64 = base64.b64encode(image_binary).decode('utf-8')

    


    # user_name= request.session.get('user_name')
    # print(user_name)
    if request.method == "POST":
        
        eventid= request.POST.get('eventid')
        


    
    # Retrieve the Razorpay order ID from the query string parameter
    # razorpay_order_id = request.GET.get('razorpay_order_id')
    
    # Retrieve the Payorderss object using the order ID
    # pay_order = Payorderss1.objects.get(id=razorpay_order_id)
    order = Payorderss2.objects.all()
    data = "Dear " + name + " , "
    data += "Invoice number: " + str(order_id) + "  "
    data += "Redirect URL: https://mihir-dave.loca.lt/redirect/"

        # Generate QR code image
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    
        # Convert image to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    # request.session['qrimg']= img
    image_bytes = buffer.getvalue()
    img_str = base64.b64encode(image_bytes).decode('utf-8')

    order = Payorderss2.objects.get(id=order_id)
    qrmodel= userqr2(orderid=order,qrcode=img_str)
    qrmodel.save()
    

    # Create a context dictionary with the order details
    context = {
         'event_name': event_name,
        'even':even,
         'loc':loc,
        'ticket_price1':ticket_price1,
        'name': name,
        'email': email,
        'mobile': mobile,
        'order_id': order_id,
        'tickettype':tickettype,
        'ticket_type':ticket_type,
        'total_price':tp,
        # 'ticket_price':ticket_price,
        'now':now,
        # 'eventid': eventid,
        # 'amount': pay_order.amount,
        'order': order,
        'api_key': settings.RAZOR_KEY_ID,
        'val2': 'val2',
        'img_qr': img_str,
        'number_ticket':number_ticket,
        'image_base64':image_base64,
    }





    subject = 'Payment Successful'
        
    email = 'davemihir1310@gmail.com'
    message1 = "Hello mr/mrs  "+ name +" your ticket has benn bocked and online payment has been done"+ "your mobilr number"+ mobile + "will be your id" + "Note that you are subscribed in an event named" + event_name
    message2=  render_to_string('invoices.html', context=context)
    message= message1+message2
    subject = 'Payment '
    email_from = 'shivdave1310@gmail.com'
    recipient_list = [email, 'davemihir1310@gmail.com']
    send_mail(subject, message1, email_from, recipient_list, fail_silently=False,html_message=message2)
        
    return render(request,'invoices.html',context)
import pdfkit
from django.http import HttpResponse
from django.template.loader import get_template
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")


import pdfkit
from django.http import HttpResponse
from django.template.loader import get_template
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")


def generate_pdf(request):
    now = datetime.datetime.now()

    name = request.session.get('name')
    email = request.session.get('email')
    mobile = request.session.get('mobile')
    tp= request.session.get('total_price')
    loc= request.session.get('loc')
    event_name= request.session.get('event_name')
    event_id= request.session.get('event_id')
    order_id= request.session.get('razor_order_id')
    even = list(event.objects.filter(eventid=event_id).values())

    # evimg= even.image
    # print(evimg)
    even1 = event.objects.get(eventid=event_id)

# get the image and read the binary data
    image_binary = even1.image.read()
    # print("checking image-------------------------------")
    # print(type(image_binary))

    # encode the binary data to base64
    image_base64 = base64.b64encode(image_binary).decode('utf-8')

    # print the encoded image
    # print(image_base64)
    tickettype= request.session.get('tickettype')
    number_ticket= request.session.get('number_ticket')
    order = Payorderss2.objects.all()
    data = "Dear " + name + " , "
    data += "Invoice number: " + str(order_id) + "  "
    data += "Redirect URL: https://mihir-dave.loca.lt/redirect/"

        # Generate QR code image
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    
        # Convert image to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    # request.session['qrimg']= img
    image_bytes = buffer.getvalue()
    img_str = base64.b64encode(image_bytes).decode('utf-8')
    # tickettype = request.session.get('tickettype')
    # ticket_type = tickettype.type_of_ticket
    ticket_type= request.session['ticket_type_real']
    ticket_price1= request.session.get('ticket_price1')
    total_price= request.session.get('total_price')
    # Get the HTML template
    template = get_template('invoices.html')
    input_file = 'invoices.html'
    # Render the template with context data
    html = template.render({'name': name, 'mobile': mobile, 'email': email, 'order_id': order_id,'ticket_type':ticket_type,'ticket_price1':ticket_price1,'img_qr': img_str,  'tickettype':tickettype,'api_key': settings.RAZOR_KEY_ID,'loc':loc,'event_name': event_name,'now':now,'val2': 'val2','number_ticket':number_ticket,'image_base64':image_base64,'total_price':total_price})


    # Define options for PDF conversion
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    # Create a PDF from the HTML template
    pdf = pdfkit.from_string(html, False, options, configuration=config)
    subject = 'Your Invoice'
    message = 'Dear {}, please find your invoice attached.'.format(name)
    email = EmailMessage(
        subject,
        message,
        'shivdave1310@gmail.com.com',
        [email],
        ['davemihir1310@gmail.com.com'], # Optional list of BCC recipients
        reply_to=['mihirdave1310@gmail.com'], # Optional list of reply-to recipients
    )
    email.attach('invoice.pdf', pdf, 'application/pdf')
    email.send()

    # Create a HTTP response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = 'attachment; filename="invoices.pdf"'
    return response






import json

def userdetail(request):
    if request.method == "POST":
        tp = request.session.get('val2')
        
        # data_str = request.body.decode('utf-8')
        number_of_ticket = int(request.POST.get('number_of_ticket'))
        eventid= request.POST.get('eventid')
        request.session['number_ticket']= number_of_ticket
        ticktype=  request.POST.get('ticket-type')
        event_id = request.session.get('event_id')
        client = Clients.objects.filter(event__eventid=eventid)

        print(event_id)


        val2= request.session.get('val2')
        print(ticktype+ "----------------------------------")
        request.session['ticket_price1']=ticktype

        
        ticket_type = int(request.POST.get('ticket-type'))
        total_price= number_of_ticket* ticket_type
        request.session['total_price'] = total_price
        request.session['no_of_tickets']= number_of_ticket
        ticket = Ticket.objects.get(eventid=event_id, ticket_price=ticket_type)
        
        ticket_type = ticket.type_of_ticket
        request.session['ticket_type_real']= ticket_type
        print(ticket_type)


        # order_id = request.session.get('order_id')

        # Retrieve the previously created object
        # order = Payorderss1.objects.get(id=order_id)
        # order= Payorderss1
        # order.number_of_tickets = number_of_ticket
        # order.tickettype = ticket_type
        # order.save()

        context= {
             'number_of_ticket':number_of_ticket,
             'ticketpr': ticktype,
             'total': total_price,
             'eventid': eventid,
             'ticket_type':ticket_type,
             'client':client,
        }
        return render(request, 'userdetail.html',context)
    return render(request,'userdetail.html')







def invoice(request):
    return render(request,'invoices.html')


import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def razorpay_payment(request):
    if request.method == 'POST':
        # Extract the payment details from the request
        data = request.POST
        amount = data['amount']
        currency = data['currency']
        payment_id = data['razorpay_payment_id']
        order_id = data['razorpay_order_id']
        signature = data['razorpay_signature']

        # Verify the payment using the Razorpay API
        client = razorpay.Client(auth=('YOUR_API_KEY', 'YOUR_API_SECRET'))
        status = client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        if status == 'valid':
            # Payment successful, update your application's database here
            return JsonResponse({'status': 'success'})
        else:
            # Payment failed
            return JsonResponse({'status': 'failure'})






def eventdash(request):
    # Retrieve the user object from the database using the user_id
    # event = Event.objects.get(eventID=2)
    events= event.objects.values('name','eventid', 'image', 'total_price','datetime_from','datetime_to')
    even =event.objects.all()

    # Pass the user object to the HTML template for rendering
    # context = {
    #     'name': events.name,
    #     'price': events.total_price,
    #     'img1': events.image,
    #     'event': events,
    #     # Add other user details as needed
    # }
    locat= location.objects.values('title','street_name','city','country')
    context = {
        'events': events,
        'even': even,
        'locat': locat,
        
    }
    return render(request, 'eventdash.html', context)

# def book(request, eventid):
#     event = event.objects.get(pk=eventid)
#     context = {'event': event}
#     return render(request, 'eventdash/book.html', context)

from django.shortcuts import render, get_object_or_404
# from .models import Event

# def booktick(request, event_id):
#     event = get_object_or_404(event, id=event_id)
#     return render(request, 'book.html', {'event': event})

def booktick(request):


    
    return render(request,'book.html')

from django.core.mail import send_mail
from django.conf import settings

# def mail(request,):
#     if request.method == "POST":
#         message= request.POST



def details(request, id):
  even = event.objects.get(eventid=id)
  loc= location.objects.get(event=id)
  request.session['loc']= loc.title +", "+ loc.street_name +" , "+ loc.city
  tick = list(Ticket.objects.filter(eventid=id).values())
  order = Payorderss2( eventid=even)
  order.save()
#   client = Clients.objects.filter(client.eventid=id)

  
  # template = event.get_template('book.html')
  context = {
    'even': even,
    'loc': loc,
    'tick': tick,
    # 'client':client,
  }
  request.session['event_name']= even.name
  request.session['event_id']= even.eventid
  event_id= request.session.get('event_id')
  event_name= request.session.get('event_name')

 
  request.session['event_id']= even.eventid
  return render( request,'book.html',context)


from django.http import JsonResponse
from .models import Ticket
def success(request):
    now = datetime.datetime.now()

    name = request.session.get('name')
    email = request.session.get('email')
    mobile = request.session.get('mobile')
    tp= request.session.get('total_price')
    loc= request.session.get('loc')
    event_name= request.session.get('event_name')
    event_id= request.session.get('event_id')
    order_id= request.session.get('razor_order_id')
    even = list(event.objects.filter(eventid=event_id).values())
    tickettype= request.session.get('tickettype')
    # tickettype = request.session.get('tickettype')
    # ticket_type = tickettype.type_of_ticket
    #ticket_type= request.session['ticket_type_real']
    ticket_price1= request.session.get('ticket_price1')
    context= {
         'name':name,
         'email':email,
         'number':mobile,
         #'ticket_type':ticket_type,
         'ticket_price1':ticket_price1,
    }
    return render(request,'success.html')

def contactus(request):
    if request.method == 'POST':
         name= request.POST.get('contact-name')
         email=request.POST.get('contact-email')
         company= request.POST.get('contact-company')
         message= request.POST.get('contact-message')
         subject = 'Customer Cair'
         message = "This message is from the company "+ company+ "  And their message is as below  " +message
         email = EmailMessage(
        subject,
        message,
        'shivdave1310@gmail.com',
        [email],
        ['davemihir1310@gmail.com'], # Optional list of BCC recipients
        reply_to=['mihirdave1310@gmail.com'], # Optional list of reply-to recipients
        )
         email.send()
         return redirect('home')
