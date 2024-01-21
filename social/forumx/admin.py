from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Profile, Thread, Post

# Unregister groups
admin.site.unregister(Group)

# Combine Profile Info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #Just display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister initial user    
admin.site.unregister(User)

# Reregister user and Profile
admin.site.register(User, UserAdmin)

# Register Thread and Post models
class PostInline(admin.StackedInline): 
    model = Post
    extra = 1

class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    inlines = [PostInline]

admin.site.register(Thread, ThreadAdmin)