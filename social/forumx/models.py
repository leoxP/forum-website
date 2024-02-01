from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

# Create threadds for the forum
class Thread(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE, 
        related_name='created_threads') #We need to access threads later on 
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title} ({self.created_at:%d-%m-%Y %H:%M}): {self.user}"

    
# Posts on threads
class Post(models.Model):
    thread = models.ForeignKey(Thread, 
        on_delete=models.CASCADE, 
        related_name='posts')
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE, 
        related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    # Keep count of likes
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f"{self.user.username} - {self.thread.title} ({self.created_at:%d-%m-%Y %H:%M}): {self.content}"

    
# Create a User Profile Model
class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE) 
   follows = models.ManyToManyField("self",
    related_name="followed_by",
    symmetrical=False, # User does not need to follow back
    blank=True # User does not need to follow anyone
    )
   
   date_modified = models.DateTimeField(User, default=timezone.now)
   # Save the location of the profile image
   profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
   
   def __str__(self):
       return self.user.username
   
# Create Profile when new user signs up (and follows itself)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)
