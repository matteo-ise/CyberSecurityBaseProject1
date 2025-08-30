from django.contrib.auth import logout as auth_logout

# Add a logout view for navigation
from django.shortcuts import redirect
def logout_view(request):
	auth_logout(request)
	return redirect('index')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import BlogPost, Comment, UserProfile
from django.db.models import Q

# HomeView: List all blog posts
class HomeView(View):
	def get(self, request):
		posts = BlogPost.objects.all().order_by('-created_date')
		return render(request, 'blog/index.html', {'posts': posts})

# FLAW 4: Security Logging and Monitoring Failures
# This login view reveals if a username exists and does not log or monitor failed attempts.
# There is no rate limiting or alerting for suspicious activity.
import logging

class LoginView(View):
	def get(self, request):
		return render(request, 'blog/login.html')
	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		# VULNERABLE: Show specific error messages revealing if username exists
		if User.objects.filter(username=username).exists():
			if user is not None:
				login(request, user)
				return redirect('index')
			else:
				error = f"Wrong password for {username}"
		else:
			error = "Username not found"
		# --- FIX (commented out): Use generic error messages and log failed attempts ---
		# error = "Invalid username or password"
		# logger = logging.getLogger("django.security")
		# logger.warning(f"Failed login attempt for username: {username} from IP: {request.META.get('REMOTE_ADDR')}")
		# Optionally: Add rate limiting and monitoring here
		return render(request, 'blog/login.html', {'error': error})

# RegisterView: Handle user registration
class RegisterView(View):
	def get(self, request):
		return render(request, 'blog/register.html')
	def post(self, request):
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if password1 != password2:
			return render(request, 'blog/register.html', {'error': 'Passwords do not match'})
		if User.objects.filter(username=username).exists():
			return render(request, 'blog/register.html', {'error': 'Username already exists'})
		user = User.objects.create_user(username=username, email=email, password=password1)
		UserProfile.objects.create(user=user)  # Create empty profile
		login(request, user)
		return redirect('index')

# PostDetailView: Show individual post with comments and handle new comment submission
class PostDetailView(View):
	def get(self, request, post_id):
		post = get_object_or_404(BlogPost, id=post_id)
		comments = Comment.objects.filter(post=post).order_by('created_date')
		return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})
	def post(self, request, post_id):
		if not request.user.is_authenticated:
			return redirect('login')
		post = get_object_or_404(BlogPost, id=post_id)
		content = request.POST.get('content')
		if content:
			Comment.objects.create(post=post, author=request.user, content=content)
		return redirect('post_detail', post_id=post.id)

# FLAW 5: Server-Side Request Forgery (SSRF)
# This code fetches the website title from any URL provided by the user without validation.
import requests
import re

from django.http import HttpResponseForbidden

@login_required
def profile_view(request, user_id=None):
	# FLAW 1: BROKEN ACCESS CONTROL
	# VULNERABLE: Any logged-in user can view any other user's profile by changing the user_id in the URL.
	if user_id is not None:
		profile = get_object_or_404(UserProfile, user__id=user_id)
		user = profile.user
		# --- FIX (uncomment the next 3 lines to secure, see README for instructions) ---
		# if request.user.id != user_id:
		#     # Only allow users to view their own profile
		#     return HttpResponseForbidden("You are not allowed to view this profile.")
	else:
		profile = get_object_or_404(UserProfile, user=request.user)
		user = request.user

	website_title = None
	if profile.website_url:
		try:
			# FLAW 5: SSRF - Fetch any URL provided by the user (SSRF)
			resp = requests.get(profile.website_url, timeout=3)
			match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE | re.DOTALL)
			if match:
				website_title = match.group(1).strip()
		except Exception:
			website_title = None
		# --- FIX (commented out): Only allow safe external domains ---
		# from urllib.parse import urlparse
		# allowed_domains = ['example.com', 'github.com']
		# parsed = urlparse(profile.website_url)
		# if parsed.hostname not in allowed_domains:
		#     website_title = None
		# else:
		#     resp = requests.get(profile.website_url, timeout=3)
		#     match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE | re.DOTALL)
		#     if match:
		#         website_title = match.group(1).strip()

	return render(request, 'blog/profile.html', {'user': user, 'profile': profile, 'website_title': website_title})

# FLAW 2: SQL Injection
# This view is vulnerable because it uses raw SQL with string concatenation.
# User input is directly inserted into the SQL query, allowing SQL injection attacks.
from django.db import connection

class SearchView(View):
	def get(self, request):
		query = request.GET.get('q', '')
		results = []
		if query:
			# VULNERABLE: Directly inserting user input into SQL string
			sql = "SELECT * FROM blog_blogpost WHERE title LIKE '%" + query + "%' OR content LIKE '%" + query + "%'"
			with connection.cursor() as cursor:
				cursor.execute(sql)  # User input is not sanitized!
				columns = [col[0] for col in cursor.description]
				for row in cursor.fetchall():
					results.append(dict(zip(columns, row)))
			# --- FIX (commented out): Use Django ORM or parameterized queries ---
			# results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
			# OR
			# cursor.execute("SELECT * FROM blog_blogpost WHERE title LIKE %s OR content LIKE %s", [f"%{query}%", f"%{query}%"])
		return render(request, 'blog/search.html', {'results': results, 'request': request})
