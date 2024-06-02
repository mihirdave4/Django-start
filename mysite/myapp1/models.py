from django.db import models
from django.core.validators import MinLengthValidator,validate_email,MaxLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from .manager import UserManager

choiceRole = (
    ("Event Coordinator", "Event Coordinator"),
    ("Event Planner", "Event Planner"),
    ("Event Manager", "Event Manager"),
    ("Registration Coordinator", "Registration Coordinator"),
    ("Volunteer Coordinator", "Volunteer Coordinator"),
    ("Marketing Coordinator", "Marketing Coordinator"),
    ("Social Media Coordinator", "Social Media Coordinator"),
    ("Logistics Coordinator", "Logistics Coordinator"),
    ("Audiovisual Coordinator", "Audiovisual Coordinator"),
    ("Catering Coordinator", "Catering Coordinator"),
    ("Security Coordinator", "Security Coordinator"),
    ("Sponsorship Coordinator", "Sponsorship Coordinator"),
    ("Speaker Coordinator", "Speaker Coordinator"),
    ("Production Assistant", "Production Assistant"),
    ("Technical Support Staff", "Technical Support Staff"),
    ("Onsite Support Staff", "Onsite Support Staff"),
    ("Event Host or Emcee", "Event Host or Emcee"),
    ("Photographer", "Photographer"),
    ("Videographer", "Videographer"),
    ("Graphic Designer", "Graphic Designer"),
    ("Web Designer", "Web Designer"),
    ("Copywriter", "Copywriter"),
    ("Event Consultant", "Event Consultant"),
    ("Data Analyst", "Data Analyst"),
    ("Event Operations Manager", "Event Operations Manager"),
    ("Sales Manager", "Sales Manager"),
    ("Finance Manager", "Finance Manager"),
    ("Customer Service Representative", "Customer Service Representative"),
    ("Event Attendant", "Event Attendant")
)



choiceCategory = (
    ("Conference", "Conference"),
    ("Seminar", "Seminar"),
    ("Symposium", "Symposium"),
    ("Workshop", "Workshop"),
    ("Trade Show", "Trade Show"),
    ("Product Launch", "Product Launch"),
    ("Networking Event", "Networking Event"),
    ("Charity Event", "Charity Event"),
    ("Fundraiser", "Fundraiser"),
    ("Gala Dinner", "Gala Dinner"),
    ("Award Ceremony", "Award Ceremony"),
    ("Sports Event", "Sports Event"),
    ("Concert", "Concert"),
    ("Festival", "Festival"),
    ("Exhibition", "Exhibition"),
    ("Art Show", "Art Show"),
    ("Fashion Show", "Fashion Show"),
    ("Film Screening", "Film Screening"),
    ("Theatre Production", "Theatre Production"),
    ("Comedy Show", "Comedy Show"),
    ("Food and Beverage Event", "Food and Beverage Event"),
    ("Corporate Event", "Corporate Event"),
    ("Religious Event", "Religious Event"),
    ("Educational Event", "Educational Event"),
    ("Political Event", "Political Event"),
    ("Cultural Event", "Cultural Event"),
    ("Social Event", "Social Event"),
    ("Health and Wellness Event", "Health and Wellness Event"),
    ("Environmental Event", "Environmental Event"),
    ("Technology Event", "Technology Event"),
)

choiceStatus = (
    ("Full-time employee", "Full-time employee"),
    ("Part-time employee", "Part-time employee"),
    ("Contract employee", "Contract employee"),
    ("Freelance employee", "Freelance employee"),
    ("Intern", "Intern"),
    ("Volunteer", "Volunteer"),
)

choicePayment = (
    ("Credit cards", "Credit cards"),
    ("Debit cards", "Debit cards"),
    ("PayPal", "PayPal"),
    ("Apple Pay", "Apple Pay"),
    ("Google Pay", "Google Pay"),
    ("Stripe", "Stripe"),
    ("Square", "Square"),
    ("Bank transfers", "Bank transfers"),
    ("Electronic wallets", "Electronic wallets"),
    ("Cryptocurrencies", "Cryptocurrencies"),
)

choiceCat = (
    ("Draft/Unpublished", "Draft/Unpublished"),
    ("Published", "Published"),
    ("Sold Out", "Sold Out"),
    ("Cancelled", "Cancelled"),
    ("Postponed", "Postponed"),
    ("Rescheduled", "Rescheduled"),
    ("Completed", "Completed"),
    ("On Hold", "On Hold"),
    ("Pending Approval", "Pending Approval"),
    ("Confirmed", "Confirmed"),
    ("Pending Payment", "Pending Payment"),
    ("Paid", "Paid"),
    ("Refunded", "Refunded"),
    ("Waiting List", "Waiting List"),
    ("Attended", "Attended"),
    ("No Show", "No Show"),
    ("VIP", "VIP"),
    ("General Admission", "General Admission"),
    ("Early Bird", "Early Bird"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=8 , null=True, blank=True)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email






class category(models.Model):
    category_id= models.AutoField(primary_key=True, verbose_name="ID")
    name= models.CharField(max_length=50)
    # parent_category= models.IntegerField(blank=True,null=True)
    image = models.ImageField(verbose_name="Image", upload_to=None, height_field=None, width_field=None, max_length=None)
    parentcategory = models.ForeignKey("self",blank=True,on_delete=models.CASCADE)
    path = models.CharField(max_length=200)
    description = models.CharField(max_length=254)
    status = models.CharField(max_length=200,choices=choiceCat,default=1)
    isDeleted = models.BooleanField(default=False)
    
    # category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_custom_set',  # Choose a suitable related name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_custom_set',  # Choose a suitable related name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )


class event(models.Model):
    eventid= models.AutoField(primary_key=True, verbose_name="EVENT ID")
    # client_id= models.ForeignKey(Client,db_column="clientID",on_delete=models.CASCADE)
    has_tickets= models.BooleanField() 
    name = models.CharField(max_length=50)
    datetime_from = models.DateTimeField()
    image= models.ImageField(null=True,blank=True,upload_to= "")

    datetime_to = models.DateTimeField()
    #category = models.ForeignKey(category, on_delete=models.CASCADE)
    total_count= models.IntegerField(blank=True,null=True)
    total_cost= models.IntegerField(blank=True,null=True)
    total_price= models.IntegerField(blank=True,null=True)
    paid_amount= models.IntegerField(blank=True,null=True)
    pending_amount= models.IntegerField(blank=True,null=True)
    hassub_event = models.BooleanField(default=False, verbose_name="Has Sub-Event")


    def __str__(self):
        return self.name
    
    def clean(self):
        if self.datetime_to < self.datetime_from:
            raise ValidationError('End time should be greater than or equal to start time.')

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Clients(models.Model):
    clientID = models.AutoField(validators=[MinLengthValidator(6)],primary_key=True)
    client_name = models.CharField(max_length=254,)
    event= models.ForeignKey(event,db_column='eventid',on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    email = models.EmailField(max_length=254)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lastLogin = models.DateTimeField()

class location(models.Model):
    title = models.CharField(max_length=50)
    street_name = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    event = models.ForeignKey(event, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class  subevent(models.Model):
    name= models.CharField(max_length=50)
    start_dat= models.DateTimeField()
    end_date= models.DateTimeField()
    event = models.ForeignKey(event, on_delete=models.CASCADE)


    def __str__(self) :
        return self.name


class sub_location(models.Model):
    sub_location= models.CharField(max_length=50)
    # eventid= models.ForeignKey(event,on_delete=models.CASCADE,db_column="eventid")
    landmark= models.CharField(max_length=50)
    event = models.ForeignKey(event, on_delete=models.CASCADE)




class Employees(models.Model):
    employeeID = models.AutoField(validators=[MinLengthValidator(6)],primary_key=True,verbose_name="Employee ID")
    firstName = models.CharField(max_length=200,verbose_name="First Name",help_text="Enter Your First Name")
    lastName = models.CharField(max_length=200,verbose_name="Last Name",help_text="Enter Your Last Name")
    email = models.EmailField(max_length=254,validators=[validate_email],help_text="Enter Valid Email")
    role = models.CharField(max_length=200,default=1,help_text="Select Job Role")
    address = models.CharField(max_length=1000,help_text="Enter Address")
    profile = models.ImageField(help_text="Upload Your Profile Picture")
    status = models.CharField(max_length=200,default=1,help_text="Choice Status")
    isDeleted = models.BooleanField(default=False)
    createdDate = models.DateTimeField()
    updatedDate = models.DateTimeField()
    lastLogin = models.DateTimeField()
    def __str__(self):
        return self.firstName

class EventTransaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    eventID = models.ForeignKey(event,on_delete=models.CASCADE,db_column='eventid')
    transactionNumber = models.CharField(max_length=36, editable=False, unique=True)
    paymentMethod = models.CharField(max_length=200,default=1)
    amount = models.IntegerField()
    createdDate = models.DateTimeField()



class eventEmployees(models.Model):
    eventID = models.ForeignKey(event, db_column='eventid', on_delete=models.CASCADE)
    employeeID = models.ForeignKey(Employees,on_delete=models.CASCADE)
    
    rolenote = models.CharField(max_length=365)


ticketchoice = (
    ("Premium", "Premium"),
    ("Gold", "Gold"),
    ("Silver", "Silver"),
)

class Ticket(models.Model):
    eventid= models.ForeignKey(event,db_column='eventid', on_delete=models.CASCADE)
    type_of_ticket= models.CharField(choices=ticketchoice,max_length=20)
    
    ticket_price= models.IntegerField()

    
class Payorderss2(models.Model):
    # orderid= models.AutoField(primary_key=True)
    id= models.CharField(primary_key=True,max_length=100, unique=True)
    name= models.CharField(max_length=100)
    number= models.IntegerField(null=True,blank=True)
    email= models.CharField(max_length=100,null=True,blank=True)
    tickettype= models.CharField(max_length=100,null=True,blank=True)
    number_of_tickets= models.IntegerField(null=True,blank=True)
    totalprice= models.IntegerField(null=True,blank=True)
    paid= models.BooleanField(default=False)
    eventid= models.ForeignKey(event,db_column='eventid',on_delete=models.CASCADE)

class SystemConfigurationm(models.Model):
    SystemConfigurationid= models.AutoField(primary_key=True)
    emailid = models.CharField(max_length=255)
    emailpassword = models.CharField(max_length=100)
    razorkeyid= models.CharField(max_length=100)
    razorsecret= models.CharField(max_length=100)
    email_port= models.IntegerField()
    email_host= models.CharField(max_length=100)
    # def __str__(self):
    #     return self.config_key

class userqr2(models.Model):
    userqrid= models.AutoField(primary_key=True)
    orderid= models.ForeignKey(Payorderss2,db_column='id',on_delete= models.CASCADE)
    qrcode= models.ImageField()
    




