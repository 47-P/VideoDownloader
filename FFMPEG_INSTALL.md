# 🎬 FFmpeg Installation Guide

## ⚠️ Why You Need FFmpeg

Your video downloader app needs **FFmpeg** to merge video and audio streams. Without it, you'll get this error:
```
ERROR: You have requested merging of multiple formats but ffmpeg is not installed.
```

## 🪟 Windows Installation (Your System)

### Method 1: Manual Installation (Recommended)

1. **Download FFmpeg:**
   - Go to [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Click **"Windows"** → **"Windows builds by BtbN"**
   - Download the latest release: `ffmpeg-master-latest-win64-gpl.zip`

2. **Extract Files:**
   - Create folder: `C:\ffmpeg`
   - Extract the ZIP file contents to `C:\ffmpeg\`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click **"Environment Variables"**
   - Under **"System Variables"**, find **"Path"**, click **"Edit"**
   - Click **"New"**, add: `C:\ffmpeg\bin`
   - Click **"OK"** on all dialogs

4. **Verify Installation:**
   - Open **Command Prompt** or **PowerShell**
   - Run: `ffmpeg -version`
   - You should see FFmpeg version information

### Method 2: Using Chocolatey (if installed)

```powershell
choco install ffmpeg
```

### Method 3: Using Winget

```powershell
winget install ffmpeg
```

### Method 4: Using Scoop

```powershell
scoop install ffmpeg
```

## 🐧 Linux Installation

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

### CentOS/RHEL/Fedora:
```bash
sudo dnf install ffmpeg
# or
sudo yum install ffmpeg
```

### Arch Linux:
```bash
sudo pacman -S ffmpeg
```

## 🍎 macOS Installation

### Using Homebrew:
```bash
brew install ffmpeg
```

### Using MacPorts:
```bash
sudo port install ffmpeg
```

## ✅ Verification

After installation, verify FFmpeg works:

```bash
ffmpeg -version
```

You should see output like:
```
ffmpeg version 4.4.2 Copyright (c) 2000-2021 the FFmpeg developers
...
```

## 🔧 Troubleshooting

### Issue: "ffmpeg is not recognized"
**Solution:** FFmpeg is not in your PATH
- Check if `C:\ffmpeg\bin` is in your system PATH
- Restart Command Prompt/PowerShell after adding to PATH
- Try restarting your computer

### Issue: "Permission denied"
**Solution:** Run Command Prompt as Administrator
- Right-click Command Prompt → "Run as administrator"

### Issue: Still getting FFmpeg errors
**Solution:** Check PATH again
- Run: `echo $env:PATH` in PowerShell
- Make sure you see `C:\ffmpeg\bin` in the output

## 🎯 What FFmpeg Does

FFmpeg is used by yt-dlp to:
- **Merge** video and audio streams
- **Convert** formats if needed
- **Extract** audio from videos
- **Process** video files

## 📝 Notes

- **Restart Required**: After adding to PATH, restart your terminal/IDE
- **System Restart**: Sometimes a full system restart is needed
- **Multiple Versions**: Make sure only one FFmpeg version is in PATH

---

**💡 Tip**: Once FFmpeg is installed and in your PATH, your video downloader app will work perfectly!
