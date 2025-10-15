# 🎬 Video Downloader Web App

A beautiful and modern web interface for downloading videos from various platforms using yt-dlp. Built with Streamlit for an intuitive user experience.

## ✨ Features

- **🎥 Multi-platform Support**: Download from YouTube, Vimeo, Dailymotion, Facebook, Twitter, Instagram, and many more
- **🎯 Quality Selection**: Choose from multiple video qualities (1080p, 720p, 480p, 360p, 240p, or best available)
- **🎵 Audio Only**: Extract audio tracks as MP3 files
- **📝 Subtitle Download**: Automatically download subtitles when available
- **📊 Progress Tracking**: Real-time download progress with file size information
- **🍪 Cookies Support**: Handle restricted content with cookies.txt files
- **🎨 Modern UI**: Beautiful and responsive interface with gradient designs
- **📱 Mobile Friendly**: Works great on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Local Development

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

### Docker Deployment

1. **Create a Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       ffmpeg \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application files
   COPY app.py .
   
   # Create downloads directory
   RUN mkdir -p /app/downloads
   
   # Expose port
   EXPOSE 8501
   
   # Run the application
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run:**
   ```bash
   docker build -t video-downloader .
   docker run -p 8501:8501 -v $(pwd)/downloads:/app/downloads video-downloader
   ```

## 🌐 Server Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push your code to GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repository**
4. **Deploy with one click!**

### Option 2: Traditional VPS/Cloud Server

1. **Set up your server** (Ubuntu/CentOS recommended)
2. **Install dependencies:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3 python3-pip -y
   
   # Install FFmpeg
   sudo apt install ffmpeg -y
   
   # Install Node.js for Streamlit (optional, for better performance)
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Deploy the application:**
   ```bash
   # Clone your repository
   git clone <your-repo-url>
   cd <your-repo-name>
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   
   # Create downloads directory
   mkdir -p downloads
   
   # Run with nohup for background execution
   nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 > app.log 2>&1 &
   ```

4. **Set up reverse proxy with Nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

### Option 3: Heroku Deployment

1. **Create a `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Add buildpacks:**
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
   ```

3. **Deploy to Heroku:**
   ```bash
   git init
   heroku create your-app-name
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

## 📁 Project Structure

```
video-downloader/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── Dockerfile         # Docker configuration (optional)
├── Procfile           # Heroku configuration (optional)
└── downloads/         # Default download directory
```

## ⚙️ Configuration

### Environment Variables

You can customize the application using these environment variables:

- `DOWNLOAD_FOLDER`: Default download directory (default: ~/Downloads)
- `STREAMLIT_SERVER_PORT`: Port to run the app (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

### Customization

The app includes extensive CSS customization for a modern look. You can modify the styles in the `app.py` file to match your brand or preferences.

## 🔒 Security Considerations

- **File Upload**: Cookies files are temporarily stored and automatically deleted after use
- **Path Traversal**: Output paths are validated to prevent directory traversal attacks
- **URL Validation**: Basic URL validation is implemented to prevent malicious inputs
- **Resource Limits**: Consider implementing download size limits for production use

## 🐛 Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg on your system
2. **Permission errors**: Ensure the app has write permissions to the download directory
3. **Memory issues**: Large files may require more server memory
4. **Network timeouts**: Increase retry settings in the code for unstable connections

### Logs

Check application logs for debugging:
```bash
# If running with nohup
tail -f app.log

# If running with Docker
docker logs <container-id>
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and yt-dlp**
