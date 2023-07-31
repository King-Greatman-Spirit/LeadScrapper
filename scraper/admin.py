from django.contrib import admin
from .models import Business

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'website', 'social_url')  # Add 'social_url' here
    list_per_page = 20

admin.site.register(Business, BusinessAdmin)
