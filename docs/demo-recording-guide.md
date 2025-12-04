# Demo Recording Guide for File Organization Bot

This guide will help you create a compelling demo video for your File Organization Bot submission.

## 🎬 Demo Structure (3-5 minutes)

### 1. Introduction (30 seconds)
**What to show:**
- Your messy Downloads folder with various file types
- Quick explanation of the problem

**Script:**
> "My Downloads folder is a mess. PDFs, images, videos, and archives all mixed together. Today I'm going to show you how I automated this away with a Python bot I built using Kiro.dev."

### 2. Installation (30 seconds)
**What to show:**
- Terminal with installation commands
- Quick pip install

**Commands to run:**
```bash
git clone https://github.com/yourusername/file-organizer-bot.git
cd file-organizer-bot
pip install -r requirements.txt
pip install -e .
```

**Script:**
> "Installation is simple. Clone the repo, install dependencies, and you're ready to go."

### 3. Organize Mode Demo (1 minute)
**What to show:**
- Current state of Downloads folder (messy)
- Run organize command
- Show the organized folder structure

**Commands to run:**
```bash
file-organizer organize
```

**Script:**
> "Let's start with organize mode. This processes all existing files in one go. Watch as it categorizes each file and moves it to the appropriate folder organized by date."

**Show:**
- Terminal output with file detection and categorization
- Before/after comparison of folder structure
- Navigate through organized folders (Pictures/2025/Dec, Documents/2025/Dec, etc.)

### 4. Watch Mode Demo (1.5 minutes)
**What to show:**
- Start watch mode
- Download or create new files
- Show real-time organization

**Commands to run:**
```bash
file-organizer watch
```

**Script:**
> "Now let's try watch mode. This monitors the folder in real-time and automatically organizes new files as they appear."

**Actions:**
1. Start watch mode
2. Download a PDF or create a test file
3. Show it immediately getting organized
4. Download an image
5. Show it going to Pictures/2025/Dec
6. Create a duplicate file
7. Show it getting renamed with (1) suffix

### 5. Key Features Highlight (1 minute)
**What to show:**
- Duplicate handling (create file.pdf, then another file.pdf)
- Cross-platform paths (show pathlib usage in code)
- Error handling (try to organize a locked file)
- Logging output

**Script:**
> "The bot handles duplicates safely by appending numeric suffixes. It works on Windows, Mac, and Linux. And it logs everything for transparency."

### 6. Code Walkthrough (30 seconds)
**What to show:**
- Quick look at the modular architecture
- Show one key component (e.g., FileCategorizer)
- Highlight clean code and docstrings

**Script:**
> "The code is clean and modular. Here's the categorizer—simple extension mappings. Everything is well-documented and easy to extend."

### 7. Testing (30 seconds)
**What to show:**
- Run pytest
- Show property-based tests
- Show coverage report

**Commands to run:**
```bash
pytest -v
pytest --cov=src/file_organizer
```

**Script:**
> "I used property-based testing with Hypothesis to catch edge cases. The tests run hundreds of scenarios automatically."

### 8. Closing (30 seconds)
**What to show:**
- Final organized folder
- GitHub repo
- Call to action

**Script:**
> "No more manual file sorting. The bot runs in the background and keeps everything organized. Check out the code on GitHub and try it yourself!"

## 🎥 Recording Tips

### Setup
1. **Clean your Downloads folder first**, then add test files
2. **Prepare test files** in advance:
   - 5-10 PDFs
   - 5-10 images (JPG, PNG)
   - 2-3 videos
   - 2-3 ZIP files
   - Some duplicates
3. **Use a screen recording tool**:
   - macOS: QuickTime or ScreenFlow
   - Windows: OBS Studio or Camtasia
   - Linux: SimpleScreenRecorder or OBS Studio
4. **Set terminal font size large** (18-20pt) for visibility
5. **Use a clean terminal theme** (dark background, high contrast)

### During Recording
1. **Speak clearly and at a moderate pace**
2. **Pause between actions** to let viewers absorb
3. **Use your mouse to highlight** important parts
4. **Show, don't just tell** - let the bot do the work
5. **Keep it under 5 minutes** - attention spans are short

### Terminal Commands to Prepare

Create test files quickly:
```bash
# Create test files
touch test.pdf test2.pdf report.pdf
touch photo.jpg screenshot.png image.gif
touch video.mp4 tutorial.mov
touch backup.zip archive.tar.gz
touch notes.txt document.docx
touch song.mp3 audio.wav
```

### What to Avoid
- ❌ Don't spend too much time on installation
- ❌ Don't show errors unless demonstrating error handling
- ❌ Don't read code line by line
- ❌ Don't go into too much technical detail
- ❌ Don't forget to show the final result

## 📝 Video Description Template

```
🤖 File Organization Bot - Automatically Organize Your Downloads Folder

Tired of manually sorting files? This Python bot automatically organizes your Downloads folder by file type and date.

✨ Features:
• Real-time monitoring with watch mode
• Batch processing with organize mode
• Smart categorization (30+ file types)
• Date-based organization (Category/YYYY/MMM)
• Duplicate handling (never overwrites)
• Cross-platform (Windows, macOS, Linux)
• Comprehensive logging

🔧 Built with:
• Python 3.8+
• watchdog for file monitoring
• Hypothesis for property-based testing
• Kiro.dev for spec-driven development

📦 Installation:
pip install file-organizer-bot

🔗 Links:
• GitHub: [your-repo-url]
• Blog Post: [your-blog-url]
• Documentation: [your-docs-url]

⏱️ Timestamps:
0:00 - Introduction
0:30 - Installation
1:00 - Organize Mode Demo
2:00 - Watch Mode Demo
3:30 - Key Features
4:00 - Code Overview
4:30 - Testing
5:00 - Conclusion

#Python #Automation #FileManagement #Kiro #DevTools
```

## 🎨 Visual Enhancements

### Terminal Styling
Use a tool like `asciinema` for terminal recording with playback controls:
```bash
asciinema rec demo.cast
# Do your demo
# Ctrl+D to stop
asciinema play demo.cast
```

### Add Captions
- Use YouTube's auto-caption feature
- Edit for accuracy
- Add timestamps in description

### Thumbnail Ideas
- Before/After split screen of Downloads folder
- Bot icon with "Automate Your Downloads"
- Terminal screenshot with colorful output

## 📤 Where to Share

1. **YouTube** - Main demo video
2. **Twitter/X** - Short clip (30 seconds)
3. **LinkedIn** - Professional audience
4. **Reddit** - r/Python, r/learnprogramming
5. **Dev.to** - Embed video in blog post
6. **GitHub README** - Link to demo video

## ✅ Pre-Recording Checklist

- [ ] Clean Downloads folder
- [ ] Prepare test files
- [ ] Increase terminal font size
- [ ] Test screen recording software
- [ ] Practice the demo once
- [ ] Check audio levels
- [ ] Close unnecessary applications
- [ ] Disable notifications
- [ ] Have script/outline ready
- [ ] Test all commands work

## 🎯 Success Metrics

A good demo should:
- ✅ Show the problem clearly
- ✅ Demonstrate the solution working
- ✅ Highlight key features
- ✅ Be easy to follow
- ✅ Inspire viewers to try it
- ✅ Be under 5 minutes

Good luck with your demo! 🚀
