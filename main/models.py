from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.conf import settings
import os

def manual_upload_path(instance, filename):
    folder = instance.name.replace(' ', '_').lower()
    return os.path.join('manuals', folder, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(null=True, blank=True)
    google_id = models.CharField(max_length=100, unique=True, null=True)

    def get_display_name(self):
        if self.user.first_name:
            return self.user.first_game
        return self.user.username
    
    def get_avatar(self):
        if self.avatar_url:
            return self.avatar_url
        
        if settings.USE_GENERATE_AVATARS:
            name = self.user.frist_name or self.user.username
            return f"https://ui-avatars.com/api/?name={name}&background=random&color=fff"
        return 'static/images/defaultuser.png'

class Manual(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=100, choices=[
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('appliances', 'Appliances'),
        ])
    
    description = models.TextField()

    image = models.ImageField(
        upload_to = manual_upload_path,
        validators = [FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])]
    )
    file = models.FileField(
        upload_to = manual_upload_path,
        validators = [FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    manual = models.ForeignKey(Manual, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)