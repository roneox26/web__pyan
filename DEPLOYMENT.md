# PythonAnywhere Deployment Guide

## Step 1: GitHub এ কোড আপলোড করুন

1. GitHub এ নতুন repository তৈরি করুন
2. আপনার local folder এ যান:
```bash
cd e:\web\ngo
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 2: PythonAnywhere Account তৈরি করুন

1. যান: https://www.pythonanywhere.com/registration/register/beginner/
2. Free account তৈরি করুন
3. Email verify করুন

## Step 3: PythonAnywhere এ Code Clone করুন

1. PythonAnywhere Dashboard এ যান
2. "Consoles" tab এ ক্লিক করুন
3. "Bash" console খুলুন
4. নিচের commands রান করুন:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

## Step 4: Virtual Environment তৈরি করুন

```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

## Step 5: Web App Setup করুন

1. "Web" tab এ যান
2. "Add a new web app" ক্লিক করুন
3. "Manual configuration" সিলেক্ট করুন
4. Python 3.10 সিলেক্ট করুন

## Step 6: WSGI Configuration

1. Web tab এ "WSGI configuration file" লিংকে ক্লিক করুন
2. সব কিছু মুছে দিয়ে এটা paste করুন:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/YOUR_REPO'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variable
os.environ['FLASK_APP'] = 'app.py'

# Import flask app
from app import app as application
```

**গুরুত্বপূর্ণ:** `YOUR_USERNAME` এবং `YOUR_REPO` আপনার নাম দিয়ে replace করুন

## Step 7: Virtual Environment Path সেট করুন

1. Web tab এ ফিরে যান
2. "Virtualenv" section এ যান
3. Path দিন: `/home/YOUR_USERNAME/.virtualenvs/myenv`

## Step 8: Static Files Setup

Web tab এ "Static files" section এ:
- URL: `/static/`
- Directory: `/home/YOUR_USERNAME/YOUR_REPO/static/`

## Step 9: Database Initialize করুন

Bash console এ:
```bash
cd YOUR_REPO
workon myenv
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

## Step 10: Reload Web App

1. Web tab এ যান
2. সবুজ "Reload" button এ ক্লিক করুন
3. আপনার URL: `YOUR_USERNAME.pythonanywhere.com`

## সমস্যা হলে:

### Error Log দেখুন:
Web tab → Log files → Error log

### Common Issues:

1. **Import Error**: Virtual environment path ঠিক আছে কিনা চেক করুন
2. **Database Error**: Database initialize করেছেন কিনা চেক করুন
3. **Static Files না দেখালে**: Static files path ঠিক আছে কিনা চেক করুন

## Update করার জন্য:

```bash
cd YOUR_REPO
git pull origin main
workon myenv
pip install -r requirements.txt
# Web tab এ গিয়ে Reload করুন
```

## Default Login:
- Admin: admin@example.com / admin123
- Staff: staff@example.com / staff123
