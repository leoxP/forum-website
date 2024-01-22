from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Thread, Post
from .forms import PostForm
from django.utils import timezone

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        threads = Thread.objects.all().order_by("-created_at")
        
    return render(request,'home.html',{"threads":threads})

def thread_posts(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = thread.posts.all().order_by("created_at")
    form = PostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.thread = thread
            post.created_at = timezone.now() 
            post.save()
            messages.success(request, "Your post has been submitted")
            return redirect('thread_posts', thread_id=thread.id)
        else:
            messages.error(request, "There was an error with your post.")

    return render(request, 'posts.html', {'thread': thread, 'posts': posts, 'form': form})

def profile_list(request):
    # You have to be logged in to see users
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles })
    else:
        messages.success(request,("You must be logged in to view profiles"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        user_posts = Post.objects.filter(user=profile.user).order_by("-created_at")
        
        # Post Form logic
        if request.method == "POST":
            # Get current user ID
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            
            #Profile saved
            current_user_profile.save()

        return render(request, 'profile.html', {"profile":profile, "user_posts": user_posts})
    else:
        messages.success(request,("You must be logged in to view profiles"))
        return redirect('home')