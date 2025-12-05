
# Copyright (c) 2025 aiMahdiX
# This file is part of the Ophthalmology Vision Test System

All notable changes to the M-Tech Clinical Vision Test System are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-04

### Added
- ✨ Professional Snellen chart vision testing system with 14 clinical levels (10/200 to 10/10)
- ✨ Dual eye testing capability (left and right eye separate assessment)
- ✨ AI-powered facial distance measurement for automatic testing distance calculation
- ✨ Hand gesture recognition using MediaPipe for intuitive directional input
- ✨ AR-enhanced camera calibration with chessboard pattern recognition
- ✨ Real-time hand detection with visual feedback
- ✨ Google Gemini AI integration for professional ophthalmologic recommendations
- ✨ Dynamic font scaling based on screen dimensions and testing distance
- ✨ Comprehensive PDF report generation with patient information
- ✨ Patient management system with registration form
- ✨ Test result comparison with previous sessions
- ✨ Settings customization menu (API key, save folder, display settings)
- ✨ Modern glass-morphism UI design with gradient backgrounds
- ✨ Multi-camera support with automatic detection and selection
- ✨ Persistent configuration storage in JSON format
- 📄 Comprehensive documentation and README
- 📝 Contributing guidelines
- 🔒 MIT License

### Features
- **Vision Testing**
  - Automated E-chart presentation
  - Distance-adaptive font sizing
  - Hand gesture input for letter direction
  - Keyboard fallback (arrow keys)

- **Computer Vision**
  - Real-time face detection
  - Automatic distance calculation
  - Camera focal length calibration
  - Hand tracking and pose estimation

- **AI Analysis**
  - Gemini AI-powered recommendations
  - Local ML-based analysis fallback
  - Risk assessment (glaucoma, amblyopia, refractive errors)

- **Data Management**
  - Professional PDF reports
  - Test result tracking and comparison
  - Patient database organization
  - Settings persistence

- **User Interface**
  - Modern, responsive design
  - Real-time feedback and status updates
  - Customizable display settings
  - Fullscreen support

### Technology Stack
- **Backend**: Python 3.8+
- **Computer Vision**: OpenCV, MediaPipe
- **Graphics**: Pygame, Pygame-GUI
- **AI**: Google Gemini API
- **Document Generation**: ReportLab
- **Configuration**: JSON

## Future Roadmap

### [1.1.0] - Planned
- [ ] Multi-language support (Persian, English, Arabic)
- [ ] Enhanced ML models for disease detection
- [ ] Voice command input
- [ ] Real-time video recording of tests
- [ ] Cloud backup integration
- [ ] Advanced statistics and trend analysis
- [ ] Export to medical formats (HL7, DICOM)
- [ ] Integration with hospital management systems

### [1.2.0] - Planned
- [ ] Mobile app companion
- [ ] Remote consultation support
- [ ] Integration with telemedicine platforms
- [ ] Advanced image analysis
- [ ] Retinal imaging support
- [ ] Eye tracking calibration
- [ ] Performance optimization
- [ ] Additional clinical tests

### [2.0.0] - Long-term Vision
- [ ] Full medical-grade certification
- [ ] Clinical trials support
- [ ] Research data export
- [ ] Multi-site management
- [ ] Advanced analytics dashboard
- [ ] AI model customization
- [ ] Hardware abstraction layer
- [ ] Cross-platform mobile apps

## Known Issues

### Current Version
- Camera calibration requires adequate lighting conditions
- Hand detection accuracy varies with lighting
- Some USB cameras may have compatibility issues
- Font rendering depends on system capabilities

### Workarounds
- Use well-lit environment for calibration
- Ensure camera is properly connected and recognized
- Try different camera indices if detection fails
- Install required fonts in system fonts directory

## Breaking Changes

None yet - v1.0.0 is the initial release.

## Installation History

### v1.0.0
Initial release with full feature set for clinical vision testing.

## Migration Guides

### From Earlier Versions
Not applicable - this is the initial release.

## Dependencies

### Core Dependencies
- opencv-python >= 4.8.0
- mediapipe >= 0.10.0
- pygame >= 2.5.0
- pygame-gui >= 0.6.9
- google-generativeai >= 0.4.0
- reportlab >= 4.0.0
- numpy >= 1.24.0

### Optional Dependencies
- tensorflow >= 2.13.0 (for advanced ML features)
- scikit-learn >= 1.3.0 (for statistical analysis)

## Deprecations

None in v1.0.0

## Security Updates

### v1.0.0
- Initial security considerations
- API key storage in local JSON (recommend encryption for production)
- Patient data stored locally (no cloud transmission of identifiable info)

## Performance Notes

### Optimization Tips
- Use well-lit environments for better performance
- Close other applications for smoother operation
- Use fullscreen mode for best display experience
- Calibrate camera once per session

### Benchmarks
- Face detection: ~30ms per frame
- Hand detection: ~20ms per frame
- Gemini API call: ~3-5 seconds
- PDF generation: ~2-3 seconds

## Contributors

- **Mehdi Ahmadi** ([@aiMahdiX](https://github.com/aiMahdiX)) - Lead Developer

## Support

For issues, questions, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/aiMahdiX/Medical_VisionTest/issues)
- Check [Troubleshooting Guide](README.md#troubleshooting) in README
- Review existing discussions and documentation

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---
**Maintained by**: [aiMahdiX](https://github.com/aiMahdiX)
