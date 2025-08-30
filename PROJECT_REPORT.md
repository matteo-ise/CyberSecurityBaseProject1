# CyberSec Blog Project – Project Report

**Repository:** https://github.com/matteo-ise/CyberSecurityBaseProject1

---

## Installation Instructions

1. Clone the repository:
   ```
   git clone https://github.com/matteo-ise/CyberSecurityBaseProject1
   cd cybersec-project
   ```
2. Set up a virtual environment:
   - Windows:
     ```
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - Mac/Linux:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Create sample data:
   ```
   python manage.py shell < management_commands_create_sample_data.py
   ```
6. Run the server:
   ```
   python manage.py runserver
   ```

---

## FLAW 1: Broken Access Control
**Source:** [blog/views.py#LXX](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#L93)

**Description:**
The profile view allows any logged-in user to view any other user's profile by changing the user_id in the URL (e.g., `/profile/3/`). This exposes sensitive information such as email, phone, and bio to unauthorized users. The flaw is in the backend logic, not just the frontend.

**How to Fix:**
Uncomment the following lines in `profile_view`:
```python
# if request.user.id != user_id:
#     return HttpResponseForbidden("You are not allowed to view this profile.")
```
This ensures only the owner can view their profile. See README for exact line numbers.

---

## FLAW 2: SQL Injection
**Source:** [blog/views.py#LXX](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#LXX)

**Description:**
The search view uses raw SQL with string concatenation, directly inserting user input into the query. This allows attackers to inject SQL (e.g., `' OR 1=1 --`).

**How to Fix:**
Replace the raw SQL with Django ORM or parameterized queries:
```python
# results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
# OR
# cursor.execute("SELECT * FROM blog_blogpost WHERE title LIKE %s OR content LIKE %s", [f"%{query}%", f"%{query}%"])
```

---

## FLAW 3: Cross-Site Scripting (XSS)
**Source:** [blog/templates/blog/post_detail.html#LXX](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/templates/blog/post_detail.html#LXX)

**Description:**
Comments are rendered using the `|safe` filter, allowing any HTML/JavaScript to execute. This enables XSS attacks if a user posts `<script>alert(1)</script>`.

**How to Fix:**
Remove the `|safe` filter in the template:
```django
{# {{ comment.content|safe }} #}
{{ comment.content }}
```

---

## FLAW 4: Security Logging and Monitoring Failures
**Source:** [blog/views.py#LXX](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#LXX)

**Description:**
The login view reveals if a username exists and does not log or monitor failed attempts. There is no rate limiting or alerting for suspicious activity.

**How to Fix:**
Use generic error messages and log failed attempts:
```python
# error = "Invalid username or password"
# logger = logging.getLogger("django.security")
# logger.warning(f"Failed login attempt for username: {username} from IP: {request.META.get('REMOTE_ADDR')}")
```

---

## FLAW 5: Server-Side Request Forgery (SSRF)
**Source:** [blog/views.py#LXX](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#LXX)

**Description:**
The profile view fetches the website title from any URL provided by the user, without validation. This allows SSRF attacks by fetching internal or malicious URLs.

**How to Fix:**
Validate URLs before fetching:
```python
# from urllib.parse import urlparse
# allowed_domains = ['example.com', 'github.com']
# parsed = urlparse(profile.website_url)
# if parsed.hostname not in allowed_domains:
#     website_title = None
# else:
#     resp = requests.get(profile.website_url, timeout=3)
#     ...
```

---

**Note:**
- All flaws are real and exploitable in the backend.
- Each fix is present in the code as a commented-out block, ready to be enabled.
- Screenshots for each flaw and fix are included in the `screenshots/` directory.
- For exact line numbers, see the repository and click the line numbers in the file browser.
