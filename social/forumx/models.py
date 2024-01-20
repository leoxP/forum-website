from django.db import models
from django.contrib.auth.models import User

# Create a User Profile Model
class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE) 
   follows = models.ManyToManyField("self",
    related_name="followed_by",
    symmetrical=False, # User does not need to follow back
    blank=True # User does not need to follow anyone
    )
   
   def __str__(self):
       return self.user.username