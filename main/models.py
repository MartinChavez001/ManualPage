from django.db import models
from django.core.validators import FileExtensionValidator

class Manual(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('appliances', 'Appliances'),
        ])
    description = models.TextField()
    file = models.FileField(
        upload_to='manuals/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name