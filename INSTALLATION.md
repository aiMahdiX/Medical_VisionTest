# Installation Guide

# Copyright (c) 2025 aiMahdiX
# This file is part of the Ophthalmology Vision Test System


Complete step-by-step instructions for setting up M-Tech Clinical Vision Test System.

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB for application and dependencies
- **Webcam**: Any USB or integrated camera

### Recommended Setup
- **OS**: Windows 11 or Ubuntu 22.04 LTS
- **Python**: 3.10 or higher
- **RAM**: 8 GB or more
- **GPU**: NVIDIA GPU with CUDA support (for faster processing)
- **Display**: 1080p or higher resolution
- **Lighting**: Well-lit room for accurate vision testing

## Installation Steps

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Choose Python 3.10 or newer
3. **Important**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Step 2: Clone the Repository

```bash
# Using HTTPS (no SSH key needed)
git clone https://github.com/aiMahdiX/Medical_VisionTest.git
cd Medical_VisionTest

# Or using SSH (if you have SSH key configured)
git clone git@github.com:aiMahdiX/Medical_VisionTest.git
cd Medical_VisionTest
```

### Step 3: Create Virtual Environment

Creating a virtual environment isolates project dependencies from system Python.

#### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal after activation.

### Step 4: Install Dependencies

```bash
# Upgrade pip (important)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

#### Installation Notes
- Installation typically takes 5-10 minutes depending on internet speed
- If installation fails, check your internet connection
- For GPU support (NVIDIA), also install:
  ```bash
  pip install tensorflow-gpu
  ```

### Step 5: Set Up Required Assets

Create the necessary directory structure and place asset files:

```
Medical_VisionTest/
├── assets/
│   ├── fonts/
│   │   └── Snellen.ttf          # ← Place Snellen font here
│   └── settings_icon.png         # ← Optional settings icon
├── 12.webp                       # ← Background image
└── 1356.jpeg                     # ← Loading screen image
```

#### Getting the Snellen Font
1. Download Snellen.ttf font file
2. Create `assets/fonts/` directory:
   ```bash
   mkdir -p assets/fonts
   ```
3. Place the font file in `assets/fonts/Snellen.ttf`

#### Using Fallback Fonts
If you don't have the Snellen font, the application will automatically use system fonts with similar characteristics.

### Step 6: Configure Gemini API

#### Option A: First Run Setup (Recommended)
1. Run the application:
   ```bash
   python Medical_vision_test.py
   ```
2. A settings dialog will appear on first run
3. Enter your Gemini API key
4. Configure other settings and save

#### Option B: Environment Variable
1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set environment variable:

**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
python Medical_vision_test.py
```

**Windows (Command Prompt)**:
```cmd
set GEMINI_API_KEY=your_api_key_here
python Medical_vision_test.py
```

**macOS/Linux**:
```bash
export GEMINI_API_KEY="your_api_key_here"
python Medical_vision_test.py
```

#### Getting Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Create new API key in default project
4. Copy the key
5. Use it in the settings menu

### Step 7: Verify Installation

```bash
# Verify Python packages
pip list | grep -E "opencv|mediapipe|pygame|google-generativeai"

# Test basic imports
python -c "import cv2, mediapipe, pygame, google.generativeai; print('✓ All packages installed')"
```

### Step 8: Run the Application

```bash
# Make sure virtual environment is activated
# (You should see (venv) prefix)

# Run the application
python Medical_vision_test.py
```

## Troubleshooting Installation

### Python Version Issues
**Problem**: "Python version 3.8+ required"
```bash
# Check Python version
python --version

# If wrong version, specify Python 3 explicitly
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
python3 -m pip install -r requirements.txt
```

### pip Installation Issues
**Problem**: `pip is not recognized`
```bash
# Windows - reinstall with pip
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

### Package Installation Failed
**Problem**: Installation hangs or fails

```bash
# Try with specific versions
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --verbose

# For Windows, try using precompiled wheels
pip install --only-binary :all: -r requirements.txt
```

### Virtual Environment Issues
**Problem**: Virtual environment not activating

```bash
# Windows - delete and recreate
rmdir /s venv
python -m venv venv
venv\Scripts\activate

# macOS/Linux
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Camera Not Detected
**Problem**: "No cameras available"

```bash
# Windows - check device manager
# macOS/Linux - check permissions
ls /dev/video*

# Give camera permissions (Linux)
sudo usermod -a -G video $USER
```

### Gemini API Key Issues
**Problem**: "Invalid API key"

1. Verify key format (should be long string)
2. Check key hasn't been revoked
3. Verify no extra spaces
4. Try setting as environment variable instead

### Import Errors
**Problem**: `ModuleNotFoundError: No module named 'X'`

```bash
# Reinstall with verbose output
pip install -r requirements.txt -v

# Check for conflicting packages
pip list

# Clean install
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## Platform-Specific Notes

### Windows 10/11
- Ensure all dependencies are installed before running
- May need Visual C++ redistributables
- USB camera drivers might need manual installation
- Windows Defender might prompt on first run

### macOS
- May require granting camera permissions in System Preferences
- Ensure Xcode Command Line Tools installed:
  ```bash
  xcode-select --install
  ```
- If experiencing frame rate issues, reduce display scaling

### Linux (Ubuntu/Debian)
- Install additional system packages:
  ```bash
  sudo apt install libsm6 libxext6 libxrender-dev
  ```
- Grant camera permissions if needed
- May require additional OpenGL libraries

## Advanced Configuration

### GPU Acceleration (NVIDIA)
```bash
# Install CUDA and cuDNN first
# Then install GPU packages
pip install tensorflow-gpu
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Performance Optimization
```bash
# Enable multi-threading
# Edit Medical_vision_test.py and increase thread count in face detection
min_detection_confidence=0.7  # Increase for faster but less accurate detection
```

### Logging Configuration
```bash
# Enable debug logging
# Set logging level to DEBUG in Medical_vision_test.py
logging.basicConfig(level=logging.DEBUG)
```

## Uninstallation

### Complete Removal

**Windows**:
```bash
# Deactivate virtual environment
deactivate

# Delete project folder
rmdir /s Medical_VisionTest

# Delete virtual environment
rmdir /s venv
```

**macOS/Linux**:
```bash
# Deactivate virtual environment
deactivate

# Delete project folder
rm -rf Medical_VisionTest

# Delete virtual environment
rm -rf venv
```

## Next Steps

1. **Read Documentation**: Review [README.md](README.md)
2. **Configure Settings**: Run app and set API key and preferences
3. **Test Vision**: Try the vision testing workflow
4. **Review Results**: Check generated PDF reports in `results/` folder
5. **Troubleshoot**: Refer to README troubleshooting section if issues arise

## Support

If you encounter issues during installation:
1. Check this guide thoroughly
2. Review [Troubleshooting](README.md#troubleshooting) section in README
3. Search [GitHub Issues](https://github.com/aiMahdiX/Medical_VisionTest/issues)
4. Open a new issue with installation details

## System Diagnostics

Create a diagnostic report:
```bash
python -c "
import sys
import platform
import cv2
import pygame
import mediapipe

print('=== System Information ===')
print(f'OS: {platform.system()} {platform.release()}')
print(f'Python: {sys.version}')
print(f'OpenCV: {cv2.__version__}')
print(f'Pygame: {pygame.version.vernum}')
print(f'MediaPipe: Latest')
print('✓ All core packages installed')
"
```

---

For detailed usage instructions, see [README.md](README.md)
