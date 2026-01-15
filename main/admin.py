from django.contrib import admin
from .models import Manual

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('name','category','uploaded_at')
    search_fields = ('name','category')