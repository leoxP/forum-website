from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Thread, Post
from .forms import PostForm, SignUpForm, ProfilePicForm
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

# Create your views here.
def home(request):
    threads=None
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

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You've been logged in. Welcome to ForumX!"))
            return redirect('home')
        else:
            messages.success(request,("Error logging in. Try Again"))
            return redirect('login')
        
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})


@login_required
def update_user(request):
    current_user = request.user
    profile_user = Profile.objects.get(user__id=request.user.id)
    
    user_form = CustomUserChangeForm(request.POST or None, request.FILES or None, instance=current_user)
    profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, "Your profile has been updated")
            return redirect('home')

    return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if post.likes.filter(id=request.user.id):
        post.likes.remove(request.user) #Unlike
    else:
        post.likes.add(request.user)
        
    return redirect(request.META.get("HTTP_REFERER"))
