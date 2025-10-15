import streamlit as st
import os
import tempfile
import yt_dlp
from pathlib import Path
import time
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Video Downloader",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .download-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .progress-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def download_video(url: str, output_folder: str, audio_only: bool, quality: str, cookies_file: Optional[str] = None, progress_bar=None, status_text=None, download_playlist: bool = False, download_subtitles: bool = False):
    """Download video using yt-dlp"""
    
    # Create a simple progress hook
    def progress_hook(d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                downloaded = d.get('downloaded_bytes', 0)
                total = d['total_bytes']
                progress = downloaded / total
                if progress_bar:
                    progress_bar.progress(progress)
                if status_text:
                    status_text.text(f"Downloading... {downloaded // 1024 // 1024}MB / {total // 1024 // 1024}MB ({progress*100:.1f}%)")
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                downloaded = d.get('downloaded_bytes', 0)
                total = d['total_bytes_estimate']
                progress = downloaded / total
                if progress_bar:
                    progress_bar.progress(progress)
                if status_text:
                    status_text.text(f"Downloading... {downloaded // 1024 // 1024}MB / ~{total // 1024 // 1024}MB ({progress*100:.1f}%)")
            else:
                if status_text:
                    status_text.text(f"Downloading... {d.get('downloaded_bytes', 0) // 1024 // 1024}MB")
        elif d['status'] == 'finished':
            if progress_bar:
                progress_bar.progress(1.0)
            if status_text:
                status_text.success("Download completed! Processing...")
        elif d['status'] == 'error':
            if status_text:
                status_text.error(f"Error: {d.get('error', 'Unknown error')}")
    
    ydl_opts = {
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
        'keepvideo': False,
        'overwrites': True,
        'continuedl': True,
        'geo_bypass': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'referer': 'https://www.google.com/',
        'progress_hooks': [progress_hook],
        'noplaylist': not download_playlist,  # Only download single video, not playlist
    }
    
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file
    
    if audio_only:
        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    else:
        if quality == 'best':
            ydl_opts['format'] = '(bestvideo[ext=mp4]+bestaudio[ext=m4a])/bestvideo+bestaudio/best'
        else:
            ydl_opts['format'] = f'(bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a])/(bestvideo[height<={quality}]+bestaudio)/best[height<={quality}]/bestvideo+bestaudio/best'
        
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    
    # Configure subtitles based on user preference
    if download_subtitles:
        ydl_opts['writesubtitles'] = True
        ydl_opts['writeautomaticsub'] = True
        ydl_opts['subtitleslangs'] = ['en']
    else:
        ydl_opts['writesubtitles'] = False
        ydl_opts['writeautomaticsub'] = False
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            
            # Display video information
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📹 Video Information")
                st.write(f"**Title:** {info.get('title', 'Unknown')}")
                duration = info.get('duration', 0)
                if duration:
                    st.write(f"**Duration:** {duration // 60}:{duration % 60:02d}")
                st.write(f"**Uploader:** {info.get('uploader', 'Unknown')}")
                view_count = info.get('view_count')
                if view_count:
                    st.write(f"**View Count:** {view_count:,}")
            
            with col2:
                if 'thumbnail' in info:
                    st.image(info['thumbnail'], caption="Video Thumbnail", width=300)
            
            # Start actual download
            ydl.download([url])
            
            return True, "Download completed successfully!"
            
    except Exception as e:
        error_msg = str(e)
        
        # Check for FFmpeg-related errors
        if "ffmpeg" in error_msg.lower() or "merging of multiple formats" in error_msg.lower():
            return False, f"FFmpeg Error: {error_msg}\n\n💡 Solution: Please install FFmpeg on your system.\nFor Windows: Download from https://ffmpeg.org/download.html and add to PATH."
        else:
            return False, f"Error during download: {error_msg}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Video Downloader</h1>
        <p>Download videos and audio from various platforms with ease</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Output folder selection
        default_output = os.path.join(os.path.expanduser("~"), "Downloads")
        output_folder = st.text_input(
            "📁 Output Folder", 
            value=default_output,
            help="Folder where downloaded files will be saved"
        )
        
        # Audio only option
        audio_only = st.checkbox(
            "🎵 Audio Only", 
            value=False,
            help="Download only the audio track as MP3"
        )
        
        # Playlist option
        download_playlist = st.checkbox(
            "📋 Download Playlist", 
            value=False,
            help="Download entire playlist (warning: can be very large)"
        )
        
        # Subtitles option
        download_subtitles = st.checkbox(
            "📝 Download Subtitles", 
            value=False,
            help="Download subtitles/captions (if available)"
        )
        
        # Quality selection
        if not audio_only:
            quality_options = ['best', '1080p', '720p', '480p', '360p', '240p']
            quality = st.selectbox(
                "🎯 Video Quality",
                options=quality_options,
                index=1,  # Default to 1080p
                help="Select the video quality to download"
            )
        else:
            quality = "best"
        
        # Cookies file upload
        cookies_file = None
        uploaded_cookies = st.file_uploader(
            "🍪 Cookies File (Optional)",
            type=['txt'],
            help="Upload cookies.txt file for restricted content"
        )
        
        if uploaded_cookies:
            # Save uploaded cookies to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
                tmp_file.write(uploaded_cookies.read().decode('utf-8'))
                cookies_file = tmp_file.name
    
    # Main content area
    st.markdown('<div class="download-card">', unsafe_allow_html=True)
    
    # URL input
    st.subheader("🔗 Enter Video URL")
    url = st.text_input(
        "Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Enter the URL of the video or playlist you want to download"
    )
    
    # Download button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        download_button = st.button(
            "🚀 Start Download",
            type="primary",
            disabled=not url.strip()
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle download
    if download_button and url.strip():
        # Validate URL
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com']):
            st.markdown('<div class="error-message">⚠️ Please enter a valid video URL from a supported platform.</div>', unsafe_allow_html=True)
            return
        
        # Create output directory if it doesn't exist
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            st.markdown(f'<div class="error-message">❌ Error creating output folder: {str(e)}</div>', unsafe_allow_html=True)
            return
        
        # Show download settings
        st.markdown('<div class="info-message">', unsafe_allow_html=True)
        st.write("**Download Settings:**")
        st.write(f"- URL: {url}")
        st.write(f"- Output Folder: {output_folder}")
        st.write(f"- Audio Only: {'Yes' if audio_only else 'No'}")
        st.write(f"- Download Playlist: {'Yes' if download_playlist else 'No'}")
        st.write(f"- Download Subtitles: {'Yes' if download_subtitles else 'No'}")
        if not audio_only:
            st.write(f"- Quality: {quality}")
        if cookies_file:
            st.write("- Cookies: Using uploaded file")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Warning for playlist downloads
        if download_playlist:
            st.markdown('<div class="error-message">⚠️ <strong>Warning:</strong> You are about to download an entire playlist. This may take a very long time and use significant storage space.</div>', unsafe_allow_html=True)
        
        # Start download
        st.subheader("📥 Download Progress")
        
        # Create progress containers
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initial status
        status_text.info("🔄 Starting download... This may take a few minutes depending on file size.")
        
        try:
            # Start the download
            success, message = download_video(url, output_folder, audio_only, quality, cookies_file, progress_bar, status_text, download_playlist, download_subtitles)
        except Exception as e:
            success = False
            message = f"Download failed: {str(e)}"
            status_text.error(f"❌ {message}")
            return
        
        if success:
            st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
            st.balloons()
            
            # Show download location
            st.markdown(f"""
            <div class="info-message">
                📁 **Download Location:** {output_folder}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
        
        # Clean up temporary cookies file
        if cookies_file and os.path.exists(cookies_file):
            try:
                os.unlink(cookies_file)
            except:
                pass
    
    # Features section
    st.markdown("""
    ## 🌟 Features
    
    - **Multi-platform Support**: Download from YouTube, Vimeo, Dailymotion, and more
    - **Quality Selection**: Choose from multiple video qualities (1080p, 720p, etc.)
    - **Audio Only**: Extract audio as MP3 files
    - **Subtitle Download**: Automatically download subtitles when available
    - **Progress Tracking**: Real-time download progress with file size information
    - **Cookies Support**: Handle restricted content with cookies.txt files
    - **Modern UI**: Beautiful and intuitive interface
    
    ## 📋 Supported Platforms
    
    - YouTube
    - Vimeo
    - Dailymotion
    - Facebook
    - Twitter
    - Instagram
    - And many more!
    
    ## ⚠️ Requirements
    
    - **FFmpeg**: Required for video/audio merging
    - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
    - **Add to PATH**: `C:\ffmpeg\bin` must be in your system PATH
    """)
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎬 Video Downloader - Powered by yt-dlp & Streamlit</p>
        <p>Made with ❤️ for easy video downloading</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
