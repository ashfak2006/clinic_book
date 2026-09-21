from django.db import models
# from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = PhoneNumberField(unique=True,region='IN')
    calling_number = PhoneNumberField(blank=True,null=True)
    profile_image = models.ImageField(upload_to='clinic/profile_images',blank=True)
    banner_image = models.ImageField(upload_to='clinic/banners',blank=True)
    email = models.EmailField()
    location_url = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    admin = models.OneToOneField('accounts.user',on_delete=models.CASCADE,related_name='clinc')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return F"{self.name}id-{self.id}"



