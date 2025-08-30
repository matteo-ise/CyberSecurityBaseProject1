from django.contrib import admin

# This file registers your models with the Django admin site.
# This allows you to manage blog posts, comments, and user profiles through the admin interface.

from django.contrib import admin
from .models import BlogPost, Comment, UserProfile

# Register the BlogPost model so it appears in the admin site
admin.site.register(BlogPost)
# Register the Comment model
admin.site.register(Comment)
# Register the UserProfile model
admin.site.register(UserProfile)
