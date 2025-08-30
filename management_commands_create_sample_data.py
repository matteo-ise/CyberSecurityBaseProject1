"""
This script creates sample data for the CyberSec Blog project.
It creates a superuser, test users, test blog posts, and comments.
Run with: python manage.py shell < management_commands_create_sample_data.py
"""
from django.contrib.auth.models import User
from blog.models import BlogPost, Comment, UserProfile

# Create superuser (if not exists)
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print('Superuser created: admin/adminpass')
else:
    print('Superuser already exists.')

# Create test users
for username in ['alice', 'bob', 'charlie']:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, f'{username}@example.com', 'testpass')
        UserProfile.objects.create(user=user, bio=f'Bio for {username}', website_url='https://example.com', phone_number='123-456-7890')
        print(f'User created: {username}/testpass')
    else:
        print(f'User already exists: {username}')

# Create test blog posts
alice = User.objects.get(username='alice')
bob = User.objects.get(username='bob')
if not BlogPost.objects.filter(title='Welcome to CyberSec Blog').exists():
    BlogPost.objects.create(title='Welcome to CyberSec Blog', content='This is the first post.', author=alice)
    BlogPost.objects.create(title='Security Tips', content='Always use strong passwords!', author=bob)
    print('Test blog posts created.')
else:
    print('Test blog posts already exist.')

# Create test comments
post = BlogPost.objects.first()
if post and not Comment.objects.filter(post=post).exists():
    Comment.objects.create(post=post, author=alice, content='Great post!')
    Comment.objects.create(post=post, author=bob, content='Thanks for sharing!')
    print('Test comments created.')
else:
    print('Test comments already exist.')
