from django.db import models
from django.core.validators import FileExtensionValidator
import os

def manual_upload_path(instance, filename):
    folder = instance.name.replace(' ', '_').lower()
    return os.path.join('manuals', folder, filename)

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

    def __str__(self):
        return self.name