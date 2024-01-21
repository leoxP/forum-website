from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('thread/<int:thread_id>/', views.thread_posts, name='thread_posts'),
]
