from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('thread/<int:thread_id>/', views.thread_posts, name='thread_posts'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('post_like/<int:pk>', views.post_like, name='post_like'),
    path('post_show/<int:pk>', views.post_show, name='post_show'),
    path('search_user/', views.search_user, name='search_user'),
]
