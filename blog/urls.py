"""
This file is for URL routing for the blog app.
You can define URL patterns for your app here.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),  # Home page
    path('login/', views.LoginView.as_view(), name='login'),  # Login page
    path('register/', views.RegisterView.as_view(), name='register'),  # Register page
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),  # Post detail
    path('profile/', views.profile_view, name='profile'),  # View own profile
    path('profile/<int:user_id>/', views.profile_view, name='profile_other'),  # FLAW: View any user's profile
    path('logout/', views.logout_view, name='logout'),  # Add logout route
    path('search/', views.SearchView.as_view(), name='search'),  # Search page
]
