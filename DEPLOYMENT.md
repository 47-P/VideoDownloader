# 🚀 Deployment Guide

## ⚠️ Important: Vercel Limitations

**Vercel is NOT recommended for this Streamlit app** because:

1. **Function Timeout**: Vercel has a 10-second timeout for hobby plans, 60 seconds for pro plans
2. **Video Downloads**: Can take several minutes, exceeding timeout limits
3. **File Storage**: No persistent storage for downloaded files
4. **Streamlit Compatibility**: Streamlit apps need persistent connections

## 🎯 Recommended Deployment Platforms

### 1. **Streamlit Cloud** (Easiest - Recommended)

**Pros:**
- ✅ Free tier available
- ✅ Built specifically for Streamlit apps
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ No timeout issues

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

**GitHub Setup:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. **Railway** (Great Alternative)

**Pros:**
- ✅ Generous free tier
- ✅ Easy deployment from GitHub
- ✅ Built-in environment variables
- ✅ Persistent storage
- ✅ No timeout issues

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub
3. Deploy your repository
4. Set environment variables if needed

### 3. **Render** (Free Tier Available)

**Pros:**
- ✅ Free tier with limitations
- ✅ Easy GitHub deployment
- ✅ Automatic SSL
- ✅ Environment variables

**Steps:**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### 4. **Heroku** (Classic Choice)

**Pros:**
- ✅ Well-established platform
- ✅ Easy deployment
- ✅ Add-ons available

**Steps:**
1. Create `Procfile` (already created)
2. Install Heroku CLI
3. Login and deploy:
```bash
heroku create your-app-name
git push heroku main
```

## 🐳 Docker Deployment (Any Platform)

If you want to use Docker on any platform:

**Files already created:**
- `Dockerfile` ✅
- `docker-compose.yml` ✅

**Deploy anywhere:**
```bash
docker build -t video-downloader .
docker run -p 8501:8501 video-downloader
```

## 🌟 **Recommended: Streamlit Cloud**

For your video downloader app, **Streamlit Cloud** is the best choice because:

1. **Purpose-built** for Streamlit applications
2. **Free tier** with generous limits
3. **No timeout issues** for long downloads
4. **Easy GitHub integration**
5. **Automatic deployments** on code changes
6. **Built-in file handling**

## 📋 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] `README.md` has clear instructions
- [ ] Test the app locally
- [ ] Consider file storage limitations
- [ ] Set up environment variables if needed

## 🔧 Environment Variables (Optional)

If you need to customize settings:

```bash
DOWNLOAD_FOLDER=/tmp/downloads
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 📝 Notes

- **File Storage**: Downloaded files are temporary on most platforms
- **Bandwidth**: Consider bandwidth limits for video downloads
- **Security**: Some platforms may restrict certain operations
- **Updates**: Keep yt-dlp updated for best compatibility

## 🚀 Quick Start with Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Video Downloader App"
   git remote add origin https://github.com/YOUR_USERNAME/video-downloader.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Deploy!

3. **Share your app**: Get a public URL like `https://your-app-name.streamlit.app`

---

**💡 Tip**: Start with Streamlit Cloud - it's the easiest and most reliable option for your Streamlit video downloader app!
