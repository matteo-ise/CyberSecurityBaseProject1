# CyberSec Blog Project

A simple Django web application for demonstrating 5 OWASP Top 10 security flaws and their fixes (commented out).

---

## Features
- Blog with posts, comments, user profiles
- 5 exploitable security flaws (with fixes commented out)
- Bootstrap UI

---

## Installation

### 1. Clone the repository
```
git clone <https://github.com/matteo-ise/CyberSecurityBaseProject1>
cd cybersec-project
```


---

# CyberSec Blog Project – Setup Instructions

## Quick Setup

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
6. **Run the development server:**
	```
	python manage.py runserver
	```

## Troubleshooting

- Make sure your virtual environment is active before running commands.
- If you get `ModuleNotFoundError`, run `pip install -r requirements.txt` again.
- If you change models, run `python manage.py makemigrations` and `python manage.py migrate`.

## requirements.txt

See the file for all required packages. Main ones:

- Django==4.2
- requests

## Project Structure

```
cybersec-project/
├── README.md
├── requirements.txt
├── manage.py
├── cybersec_app/
│   └── ...
├── blog/
│   ├── templates/blog/
│   └── ...
├── management_commands_create_sample_data.py
└── screenshots/
```