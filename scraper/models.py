from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    website = models.URLField(default="")
    social_url = models.URLField(default="")  # Add the Social URL field

    def __str__(self):
        return self.name
    
