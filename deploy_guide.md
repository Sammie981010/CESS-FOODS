# HireWise Web Hosting Guide

## 🌐 Hosting Options

### 1. **Heroku (Recommended - Free)**
```bash
# Install Heroku CLI
# Create account at heroku.com

# Deploy steps:
git init
git add .
git commit -m "Initial commit"
heroku create hirewise-platform
git push heroku main
```

### 2. **PythonAnywhere (Free)**
- Upload files to pythonanywhere.com
- Set up web app with Flask
- Point to hirewise_web.py

### 3. **Render (Free)**
- Connect GitHub repo to render.com
- Auto-deploy from repository
- Uses Procfile automatically

### 4. **Railway (Free)**
- Connect repo to railway.app
- Automatic deployment
- Custom domain available

## 🚀 Quick Local Test
```bash
pip install flask
python hirewise_web.py
# Visit: http://localhost:5000
```

## 📁 Required Files
- hirewise_web.py (main app)
- requirements_web.txt (dependencies)
- Procfile (for deployment)
- JSON data files (auto-created)

## 🔧 Features Included
- ✅ Responsive web interface
- ✅ Professional listings
- ✅ Job posting system
- ✅ User registration
- ✅ API endpoints
- ✅ Mobile-friendly design

## 📞 Support
Contact: hirewise0@gmail.com
Phone: 0727335236