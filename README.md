# M-Tech Clinical Vision Test System
# Copyright (c) 2025 aiMahdiX
# This file is part of the Ophthalmology Vision Test System


A professional, AI-powered vision testing application that uses computer vision and machine learning to conduct automated eye examinations with Snellen chart analysis and Gemini AI-driven recommendations.

**Developed by [Mehdi Ahmadi](https://github.com/aiMahdiX)**

---

## 📋 Overview

The M-Tech Clinical Vision Test System is a comprehensive desktop application designed for professional vision assessment. It combines advanced computer vision techniques with artificial intelligence to provide accurate eye health analysis and recommendations. The system supports multi-eye testing, distance measurement, hand gesture recognition for directional input, and generates detailed PDF reports.

## ✨ Key Features

### Vision Testing Capabilities
- **Snellen Chart Analysis**: Automated E-chart presentation with 14 clinical levels (10/200 to 10/10)
- **Dual Eye Testing**: Separate assessment for left and right eyes
- **Distance Measurement**: AI-powered facial detection to calculate optimal testing distance
- **Adaptive Font Sizing**: Automatic scaling based on actual screen dimensions and testing distance
- **Hand Gesture Recognition**: Uses MediaPipe for intuitive directional input (Up, Down, Left, Right)

### Advanced Features
- **Camera Calibration**: AR-enhanced chessboard calibration for accurate focal length measurement
- **AI-Powered Analysis**: Google Gemini AI provides professional ophthalmologic recommendations
- **Patient Management**: Complete patient registration with personal and contact information
- **Result Tracking**: Comparison with previous test results and trend analysis
- **Professional Reports**: PDF generation with test results, recommendations, and patient photos

### UI/UX Features
- **Modern Glass-Morphism Design**: Contemporary visual interface with gradient backgrounds
- **Real-time Hand Detection**: Live feedback for user gestures and hand position
- **Dynamic Settings Menu**: Customizable API keys, save folders, display settings
- **First-Run Configuration**: Automatic setup wizard for initial configuration

## 🛠️ System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11, macOS, or Linux
- **Webcam/Camera**: For video capture and face detection
- **Display**: Recommended 1080p or higher
- **RAM**: Minimum 4GB (8GB recommended)

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| opencv-python | Latest | Computer vision and image processing |
| mediapipe | Latest | Hand and face detection |
| pygame | Latest | Graphics rendering and UI |
| pygame-gui | Latest | GUI components |
| google-generativeai | Latest | Gemini AI integration |
| reportlab | Latest | PDF report generation |
| numpy | Latest | Numerical computations |
| matplotlib | Latest | Medical chart generation |

## 🚀 Installation

### Clone the Repository
```bash
git clone https://github.com/aiMahdiX/Medical_VisionTest.git
cd Medical_VisionTest
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Assets
Create the following directory structure:
```
Medical_VisionTest/
├── assets/
│   └── fonts/
│       └── Snellen.ttf          # Snellen chart font
│   └── settings_icon.png         # Optional settings button icon
├── 12.webp                       # Background image
├── 1356.jpeg                     # Loading screen image
└── Medical_vision_test.py
```

## 🔑 Configuration

### Gemini API Setup
1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. The application will prompt for API key on first run
3. Alternatively, set environment variable:
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY = "your_api_key_here"
   
   # Windows (CMD)
   set GEMINI_API_KEY=your_api_key_here
   
   # macOS/Linux
   export GEMINI_API_KEY="your_api_key_here"
   ```

### Application Settings
On first launch, configure:
- **API Key**: Google Gemini API key for AI analysis
- **Save Folder**: Directory for storing test results (default: `./results`)
- **Display Settings**: Fullscreen mode, screen diagonal (inches)
- **Screen Calibration**: Input your monitor's diagonal size for accurate font scaling

## 🎯 Usage

### Starting the Application
```bash
python Medical_vision_test.py
```

### Testing Workflow
1. **Initialization**: Select camera and complete first-run setup (if needed)
2. **Patient Registration**: Fill patient information form
3. **Camera Calibration**: AR-assisted chessboard calibration for focal length
4. **Vision Test**:
   - Cover left eye, perform Snellen chart test
   - Cover right eye, perform Snellen chart test
   - Use hand gestures or arrow keys to indicate letter orientation
5. **Analysis**: AI-powered recommendation generation
6. **Report**: PDF report saved with test results and analysis

### Input Methods
- **Hand Gesture**: Point extended hand in direction of letter rotation
- **Keyboard**: Arrow keys (↑ Up, ↓ Down, ← Left, → Right)
- **Voice**: Voice input support (future enhancement)

## 📊 Output and Reports

The system generates comprehensive PDF reports containing:
- Patient demographics and medical ID
- Test results for both eyes (Snellen levels)
- Comparison with previous test sessions
- AI-generated ophthalmologic analysis
- Professional recommendations
- Patient photo (if provided)

Results are organized by patient:
```
results/
└── FirstName_LastName/
    ├── vision_test_20240112_143022.pdf
    ├── vision_test_20240115_095301.pdf
    └── previous_results.txt
```

## 🔐 Data Privacy & Security

- **Local Processing**: Patient data stored locally in results folder
- **API Calls**: Only vision test summary sent to Gemini API (no identifiable info)
- **Secure Settings**: Configuration saved in encrypted JSON format
- **No Cloud Backup**: Results remain on local system by default

## 🏥 Clinical Notes

### Snellen Chart Levels
The application tests 14 clinical levels based on standard ophthalmologic assessment:
- 10/200 to 10/10 (visual acuity from legal blindness to better than average vision)

### Distance Calibration
- Standard testing distance: 1 meter (adjustable)
- AI calculates actual distance using facial width detection
- Font sizes automatically scaled for accurate visual angle

### Accuracy Considerations
- Lighting conditions affect face detection accuracy
- Camera calibration improves distance measurement precision
- Multiple calibration images (15) recommended for best results

## 🚨 Troubleshooting

### Camera Not Detected
- Check camera permissions in system settings
- Try different camera indices (0, 1, 2...)
- Ensure USB camera is properly connected

### Calibration Fails
- Ensure adequate lighting on chessboard
- Use 9×6 standard checkerboard pattern
- Capture images from various angles

### API Error
- Verify Gemini API key is valid
- Check internet connection
- Monitor API rate limits

### Font Issues
- Ensure `Snellen.ttf` font file exists in `assets/fonts/`
- Fallback to system fonts if custom font unavailable

## 📝 Development

### Project Structure
```
Medical_VisionTest/
├── Medical_vision_test.py      # Main application
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
├── LICENSE                      # MIT License
├── assets/                      # Static resources
│   ├── fonts/
│   │   └── Snellen.ttf
│   └── settings_icon.png
├── results/                     # Test results storage
├── 12.webp                      # Background image
└── 1356.jpeg                    # Loading image
```

### Key Components

#### Medical Vision Testing
- `perform_full_test_for_eye()`: Conducts full eye test sequence
- `compute_font_sizes()`: Calculates Snellen chart font sizes
- `adjust_font_sizes()`: Adapts sizes for measured distance

#### Computer Vision
- `calibrate_camera()`: AR-assisted camera calibration
- `detect_distance()`: Facial distance measurement
- `get_extended_hand_direction()`: Hand gesture recognition

#### AI Integration
- `get_gemini_recommendation()`: Generates AI analysis
- Test summary with clinical findings sent to Gemini

#### Data Management
- `save_results()`: PDF report generation
- `generate_comparison_text()`: Compares with previous tests
- `load_settings()` / `mark_configured()`: Configuration management

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mehdi Ahmadi**
- GitHub: [@aiMahdiX](https://github.com/aiMahdiX)
- Email: Contact via GitHub profile

## 🙏 Acknowledgments

- Google Gemini AI for advanced analysis capabilities
- MediaPipe by Google for computer vision models
- OpenCV for image processing
- Pygame for graphics rendering

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/aiMahdiX/Medical_VisionTest/issues)
- Check existing documentation and troubleshooting guide

## 🔮 Future Enhancements

- [ ] Multi-language support (Persian, English, Arabic)
- [ ] Cloud backup integration for secure data storage
- [ ] Advanced ML-based eye disease detection
- [ ] Voice input for directional commands
- [ ] Mobile app companion for data viewing
- [ ] Export to standard medical formats (HL7, DICOM)
- [ ] Integration with hospital management systems
- [ ] Real-time video streaming for remote consultation

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Maintained by**: [aiMahdiX](https://github.com/aiMahdiX)

## License

See [LICENSE](LICENSE).

## Disclaimer

This tool is experimental. Use at your own risk.

---

© 2025 aiMahdiX
# Medical_VisionTest 
# Clinic
# eyes_health

