# def email_config():
from .models import SystemConfigurationm



def setup_system_configuration():
    # Check if a SystemConfigurationm object already exists in the database
    if SystemConfigurationm.objects.count() == 0:
        # Create a new SystemConfigurationm object with default values
        config = SystemConfigurationm(emailid='shivdave1310@gmail.com',
                                      emailpassword='dxgvkqlvcuwsdxdn',
                                      razorkeyid='rzp_test_Ft3GYqM2LEGC5R',
                                      razorsecret='2qUiGDUJinOCVIgGR0Q1rkDO',
                                      email_port=587, email_host='smtp.gmail.com')
        # Save the new object to the database
        config.save()
