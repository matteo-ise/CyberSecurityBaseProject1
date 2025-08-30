
# CyberSec Blog Project – Project Report

**Repository:** https://github.com/matteo-ise/CyberSecurityBaseProject1

---

## Installation Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/matteo-ise/CyberSecurityBaseProject1
   cd cybersec-project
   ```
2. **Set up a virtual environment:**
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
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```
   python manage.py migrate
   ```
5. **Create sample data:**
   ```
   python manage.py shell < management_commands_create_sample_data.py
   ```
6. **Run the server:**
   ```
   python manage.py runserver
   ```

---

## FLAW 1: Broken Access Control (OWASP A01:2021)
**Source:** [blog/views.py#L103](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#L103)

**Description:**
The profile view allows any authenticated user to access the private profile data of any other user by manipulating the `user_id` parameter in the URL (e.g., `/profile/3/`). This exposes sensitive information such as email, phone, and bio, violating the principle of least privilege. The flaw is present in the backend logic and is not mitigated by frontend controls.

**How to Test:**
1. Log in as `alice` (`testpass`).
2. Visit `/profile/3/` to view Bob's profile. Alice will see Bob's private data.
3. Repeat for other user IDs to confirm the flaw.

**How to Fix:**
Uncomment the following lines in `profile_view`:
```python
# if request.user.id != user_id:
#     return HttpResponseForbidden("You are not allowed to view this profile.")
```
This enforces that users can only view their own profile.

**Screenshot:**
- flaw-1-before-1.png: Alice viewing Bob's profile (private data visible).
- flaw-1-after-1.png: Alice denied access after fix (forbidden message).

---

## FLAW 2: SQL Injection (OWASP A03:2021)
**Source:** [blog/views.py#L150](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#L150)

**Description:**
The search functionality is vulnerable to SQL injection because it constructs SQL queries by concatenating unsanitized user input. An attacker can manipulate the query to return all posts or attempt malicious actions.

**How to Test:**
1. Go to `/search/`.
2. Enter `' OR 1=1 --` in the search box and submit.
3. All blog posts will be shown, regardless of the search term.
4. Try other payloads like `' OR 'a'='a` or `%` to confirm the flaw.

**How to Fix:**
Replace the raw SQL with Django ORM or parameterized queries:
```python
# results = list(BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)))
```
This ensures user input is safely handled.

**Screenshot:**
- flaw-2-before-1.png: Search with injection payload, all posts shown.
- flaw-2-after-1.png: Same payload after fix, none shown.

---

## FLAW 3: Cross-Site Scripting (XSS, OWASP A03:2021)
**Source:** [blog/templates/blog/post_detail.html#L19](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/templates/blog/post_detail.html#L19)

**Description:**
User comments are rendered using the `|safe` filter, allowing any HTML or JavaScript to execute. This enables XSS attacks if a user posts `<script>alert(1)</script>`.

**How to Test:**
1. Log in and view any blog post.
2. Add a comment: `<script>alert(1)</script>`
3. The script will execute in the browser, proving the flaw.

**How to Fix:**
Remove the `|safe` filter in the template:
```django
{# {{ comment.content|safe }} #}
{{ comment.content }}
```
This ensures user input is properly escaped.

**Screenshot:**
- flaw-3-before-1.png: Comment with script.
- flaw-3-before-2.png: executes (alert box).
- flaw-3-after-1.png: Comment is shown as text after fix.

---

## FLAW 4: Security Logging and Monitoring Failures (OWASP A09:2021)
**Source:** [blog/views.py#L23](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#L23)

**Description:**
The login view reveals whether a username exists and does not log or monitor failed login attempts. There is no rate limiting or alerting for suspicious activity, making brute-force and enumeration attacks easier.

**Note:**
For demonstration, you will find instructional comments for FLAW 4 in two places:
- In `views.py` (backend): Explains the vulnerable logic and how to fix it in the Python code.
- In `login.html` (frontend): Explains how to toggle the error message display for testing.
This is intentional, so you can easily test and screenshot both the backend flaw and the user-facing result. Toggle the flaw/fix in both files as described in the comments for a complete demonstration.

**How to Test:**
1. Attempt to log in with a non-existent username.
2. Observe the error message: "Username not found".
3. Try a valid username with a wrong password: "Wrong password for alice".

**How to Fix:**
Use generic error messages in views.py and log failed attempts:
```python
# error = "Invalid username or password"
# logger = logging.getLogger("django.security")
# logger.warning(f"Failed login attempt for username: {username} from IP: {request.META.get('REMOTE_ADDR')}")
```
This prevents information leakage and enables monitoring.

**Screenshot:**
- flaw-4-before-1.png: Specific error messages shown.
- flaw-4-after-1.png: Generic error message after fix.

---

## FLAW 5: Server-Side Request Forgery (SSRF, OWASP A10:2021)
**Source:** [blog/views.py#L115](https://github.com/matteo-ise/CyberSecurityBaseProject1/blob/main/blog/views.py#L115)

**Description:**
The profile view fetches the website title from any URL provided by the user, without validation. This allows SSRF attacks by fetching internal or malicious URLs, potentially exposing internal services.

**How to Test:**
1. Edit your profile and set the website URL to an internal or malicious address (e.g., `http://localhost:8000/`).
2. View your profile. The server will fetch and display the website title.

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
This restricts requests to safe domains only.

**Screenshot:**
- flaw-5-before-1.png: Profile page.
- flaw-5-before-2.png: title from arbitrary URL.
- flaw-5-before-3.png: Profile page fetches and displays title from arbitrary URL.
- flaw-5-after-1.png: After fix, only safe domains allowed or title not shown.

---

**Notes:**
- All flaws are real and exploitable in the backend.
- Each fix is present in the code as a commented-out block, ready to be enabled.
- Screenshots for each flaw and fix are included in the `screenshots/` directory.
- For exact line numbers, see the repository and click the line numbers in the file browser.
