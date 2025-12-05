# Contributing to M-Tech Clinical Vision Test System

# Copyright (c) 2025 aiMahdiX
# This file is part of the Ophthalmology Vision Test System

Thank you for your interest in contributing to the M-Tech Clinical Vision Test System! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive in all interactions
- Help create a welcoming environment for all contributors
- Report any inappropriate behavior to the maintainers

## How to Contribute

### Reporting Bugs

Before creating a bug report, please search the [issue tracker](https://github.com/aiMahdiX/Medical_VisionTest/issues) to ensure the issue hasn't already been reported.

When reporting a bug, include:
- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs. actual behavior
- **Screenshots or videos** if applicable
- **System information**: OS, Python version, camera model
- **Logs** from the application (check terminal output)

### Suggesting Enhancements

Enhancement suggestions are always welcome! When suggesting an enhancement:
- Use a clear, descriptive title
- Provide a detailed description of the proposed feature
- List some examples of how the feature would be used
- Explain why this enhancement would be useful

### Pull Requests

#### Before Starting
1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Medical_VisionTest.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Set up development environment:
   ```bash
   cd Medical_VisionTest
   pip install -r requirements.txt
   ```

#### Making Changes
- Write clear, descriptive commit messages
- Follow the existing code style (PEP 8)
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation if necessary

#### Code Style Guidelines
```python
# Use descriptive variable names
# example: face_width, not fw

# Use type hints where possible
def calculate_distance(focal_length: float, object_width: float) -> float:
    """Calculate distance using perspective formula."""
    pass

# Add docstrings to functions
def my_function():
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description
        
    Returns:
        Description of return value
    """
    pass

# Use f-strings for formatting
logging.info(f"Calibrated focal length: {focal_length:.2f}px")
```

#### Testing
Before submitting a pull request:
- Test the application end-to-end
- Verify all features work as expected
- Check for any error messages or warnings
- Test with different camera configurations if possible

#### Submitting a Pull Request
1. Push your branch: `git push origin feature/your-feature-name`
2. Create a Pull Request on GitHub
3. Fill out the PR template with:
   - Description of changes
   - Related issue(s)
   - Testing performed
   - Screenshots/videos if applicable
4. Wait for review and address any feedback

## Development Setup

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Setup Steps
```bash
# Clone the repository
git clone https://github.com/aiMahdiX/gemini_sys_admin.git
cd gemini_sys_admin

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python Medical_vision_test.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_vision.py

# Run with coverage
pytest --cov=. --cov-report=html
```

## Project Structure

```
Medical_VisionTest/
├── Medical_vision_test.py       # Main application
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── CONTRIBUTING.md               # This file
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
├── assets/
│   ├── fonts/
│   │   └── Snellen.ttf           # Snellen chart font
│   └── settings_icon.png         # Settings icon
├── results/                      # Test results (generated)
├── 12.webp                       # Background image
└── 1356.jpeg                     # Loading screen image
```

## Key Components

### Vision Testing
- `perform_full_test_for_eye()`: Main testing function
- `compute_font_sizes()`: Font size calculation
- `adjust_font_sizes()`: Distance-based scaling

### Computer Vision
- `calibrate_camera()`: AR-assisted calibration
- `detect_distance()`: Facial distance measurement
- `get_extended_hand_direction()`: Hand gesture recognition

### AI Integration
- `get_gemini_recommendation()`: AI analysis
- `get_gemini_api()`: API calls

### Data Management
- `save_results()`: PDF generation
- `load_settings()`: Settings management
- `generate_comparison_text()`: Result comparison

## Documentation

When adding new features:
- Update README.md with new features
- Add docstrings to all functions
- Include usage examples
- Document configuration options

## Commit Message Guidelines

```
# Good commit message
Fix hand detection false positives in calibration

- Improved hand tracking accuracy
- Added threshold validation
- Fixes #123

# Format: [Type] Description
# Types: Feature, Fix, Docs, Style, Refactor, Perf, Test
```

## Areas for Contribution

We're looking for help with:
- **Bug fixes**: See open issues
- **Performance improvements**: Optimize computer vision pipeline
- **Feature requests**: Implement suggested features
- **Documentation**: Improve README, add tutorials
- **Testing**: Write unit and integration tests
- **Localization**: Add language support
- **UI/UX**: Improve interface design

## Questions?

- Open an issue with tag `question`
- Contact maintainers on GitHub
- Check existing discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to M-Tech Clinical Vision Test System! 🎉
