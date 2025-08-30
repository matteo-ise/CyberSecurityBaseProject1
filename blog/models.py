
from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model


# This file defines the models (database structure) for the blog app.
# Each model is a Python class that subclasses django.db.models.Model.

# BlogPost model represents a blog post written by a user.
class BlogPost(models.Model):
	title = models.CharField(max_length=200)  # Title of the post
	content = models.TextField()              # Content of the post
	author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User who wrote the post
	created_date = models.DateTimeField(auto_now_add=True)      # Date and time the post was created

	def __str__(self):
		# This method returns a readable string for each BlogPost object
		return f"{self.title} by {self.author.username}"

# Comment model represents a comment on a blog post.
class Comment(models.Model):
	post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)  # Link to the related BlogPost
	author = models.ForeignKey(User, on_delete=models.CASCADE)    # Link to the User who wrote the comment
	content = models.TextField()                                  # Content of the comment
	created_date = models.DateTimeField(auto_now_add=True)        # Date and time the comment was created

	def __str__(self):
		# This method returns a readable string for each Comment object
		return f"Comment by {self.author.username} on {self.post.title}"

# UserProfile model extends the built-in User model with extra fields.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User
	bio = models.TextField(blank=True)                           # Short biography
	website_url = models.URLField(blank=True)                    # Personal website URL
	phone_number = models.CharField(max_length=20, blank=True)   # Phone number

	def __str__(self):
		# This method returns a readable string for each UserProfile object
		return f"Profile of {self.user.username}"
