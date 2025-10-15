#!/bin/bash

# Video Downloader App Deployment Script

echo "🚀 Video Downloader App Deployment Helper"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git branch -M main
fi

# Check if all files are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Adding and committing changes..."
    git add .
    git commit -m "Update video downloader app"
else
    echo "✅ All files are already committed"
fi

echo ""
echo "🎯 Deployment Options:"
echo "1. Streamlit Cloud (Recommended)"
echo "2. Railway"
echo "3. Render"
echo "4. Heroku"
echo "5. Docker (Any platform)"

echo ""
echo "📋 Next Steps:"
echo ""

echo "🌟 For Streamlit Cloud (Recommended):"
echo "1. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git push -u origin main"
echo ""
echo "2. Go to https://share.streamlit.io"
echo "3. Connect your GitHub repository"
echo "4. Deploy with one click!"
echo ""

echo "🚂 For Railway:"
echo "1. Push to GitHub (same as above)"
echo "2. Go to https://railway.app"
echo "3. Connect GitHub and deploy"
echo ""

echo "🎨 For Render:"
echo "1. Push to GitHub (same as above)"
echo "2. Go to https://render.com"
echo "3. Create Web Service from GitHub"
echo "4. Set start command: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0"
echo ""

echo "🐳 For Docker:"
echo "docker build -t video-downloader ."
echo "docker run -p 8501:8501 video-downloader"
echo ""

echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "✨ Happy deploying!"
