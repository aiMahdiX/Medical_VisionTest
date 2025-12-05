# Copyright (c) 2025 aiMahdiX
# This file is part of the Ophthalmology Vision Test System

# Google Gemini API Setup Guide


Complete guide for setting up and configuring Google Gemini API for the M-Tech Clinical Vision Test System.

## Overview

The M-Tech Clinical Vision Test System uses Google's Gemini AI to provide professional ophthalmologic recommendations based on vision test results. This guide walks you through obtaining and configuring your API key.

## Getting Your API Key

### Step 1: Access Google AI Studio

1. Open your web browser
2. Navigate to [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Sign in with your Google account (create one if needed)

### Step 2: Create API Key

1. Click the **"Create API Key"** button
2. Choose **"Create API key in new project"**
3. Google will generate your unique API key
4. Copy the API key (you'll see a copy button)
5. Store it safely - you'll need it for configuration

## API Key Format

Your API key should look similar to this:
```
AIzaSyDxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Important**: Never share your API key publicly or commit it to version control.

## Configuration Methods

### Method 1: First-Run Configuration (Recommended)

When you run the application for the first time:

1. Launch the application:
   ```bash
   python Medical_vision_test.py
   ```

2. A **Settings Dialog** will appear automatically
3. Paste your API key in the **"API Key"** field
4. Click **"Save Settings"**
5. The key is securely stored for future sessions

### Method 2: Environment Variable

Set the API key as an environment variable before running the application.

#### Windows (PowerShell)
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
python Medical_vision_test.py
```

#### Windows (Command Prompt)
```cmd
set GEMINI_API_KEY=your_api_key_here
python Medical_vision_test.py
```

#### macOS/Linux (Bash/Zsh)
```bash
export GEMINI_API_KEY="your_api_key_here"
python Medical_vision_test.py
```

#### macOS/Linux (Persistent)
Add to your shell profile file (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Method 3: Configuration File

The application saves settings in `.visiontest_settings.json`:

```json
{
    "api_key": "your_api_key_here",
    "save_folder": "/path/to/results",
    "fullscreen": true,
    "screen_diag_in": 15.0
}
```

**Note**: Store this file securely and never commit to version control.

## API Key Management

### Checking Your API Keys

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project from dropdown
3. Navigate to **Credentials**
4. You'll see all your API keys listed

### Revoking an API Key

If you suspect your key is compromised:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Credentials**
3. Find your API key in the list
4. Click **Delete** (trash icon)
5. Confirm deletion
6. Generate a new key using the steps above

### Regenerating an API Key

If you want to reset without revoking:

1. Revoke the old key (see above)
2. Create a new API key
3. Update your configuration with the new key

## Usage Limits and Pricing

### Free Tier
- **Rate Limit**: 60 requests per minute
- **Daily Limit**: 1,500 requests per day
- **Cost**: Free up to limits

### Quota Management

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services > Quotas**
3. Find "Generative Language API"
4. View current usage and limits

### Monitoring Usage

```bash
# In application logs, you'll see API calls like:
# INFO: Generating recommendation via Gemini API...
# INFO: ✓ Recommendation received
```

## Troubleshooting

### "Invalid API Key" Error

**Problem**: Application shows "Invalid API key"

**Solutions**:
1. Verify the key is copied completely (no extra spaces)
2. Ensure the key hasn't been revoked
3. Check you're using the correct key (not from old project)
4. Try regenerating a new API key
5. Restart the application

### "API Key Not Set" Error

**Problem**: Settings dialog appears even after saving key

**Solutions**:
1. Check `.visiontest_settings.json` file exists in project folder
2. Verify the JSON syntax is valid:
   ```bash
   python -m json.tool .visiontest_settings.json
   ```
3. Ensure you have write permissions to the project folder
4. Re-enter the key and save again

### "Rate Limit Exceeded" Error

**Problem**: Getting rate limit errors during tests

**Solutions**:
1. Wait a few minutes before trying again (60 requests/minute limit)
2. Upgrade to paid plan if needed more capacity
3. Batch your requests (reduce frequency of tests)
4. Use local ML analysis as fallback (implemented in code)

### "Network Error" When Calling API

**Problem**: Unable to connect to Gemini API

**Solutions**:
1. Check your internet connection
2. Verify firewall isn't blocking API calls
3. Check Google's status page for API outages
4. Try again in a few minutes
5. Application uses fallback local analysis if API fails

### Key Not Being Used

**Problem**: Application shows "Using local analysis" instead of AI recommendations

**Solutions**:
1. Verify API key is set correctly
2. Check internet connectivity
3. Review application logs for specific error
4. Try regenerating API key
5. Check API quota hasn't been exceeded

## Security Best Practices

### Protecting Your API Key

1. **Never commit to version control**
   - Add `.visiontest_settings.json` to `.gitignore`
   - Don't share the file publicly

2. **Use environment variables** for sensitive deployments
3. **Rotate keys periodically** (recommend every 3-6 months)
4. **Monitor usage** in Google Cloud Console
5. **Use IP restrictions** if deploying on fixed server

### .gitignore Configuration

The project includes `.gitignore` with:
```
# Project specific
.visiontest_settings.json
.visiontest_configured
camera_focals.json
```

Ensure these lines are in your `.gitignore` file.

## Advanced Configuration

### Setting API Quotas

In Google Cloud Console:

1. Go to **APIs & Services > Quotas**
2. Find "Generative Language API"
3. Click the API name
4. Set custom quotas:
   - **Requests per minute**: Adjust as needed
   - **Requests per day**: Cap daily usage

### Using Different Models

By default, the application uses `gemini-2.0-flash`. To use a different model:

1. Edit `Medical_vision_test.py`
2. Find line with `model = "gemini-2.0-flash"`
3. Change to desired model:
   ```python
   model = "gemini-1.5-pro"  # More powerful but slower
   model = "gemini-1.5-flash"  # Faster, less capable
   ```

### Regional Settings

Google Gemini API is available globally. If you're in a region with restrictions:

1. Use VPN if needed
2. Check Google's regional availability
3. Contact Google support for enterprise solutions

## Testing Your Setup

### Test API Connection

```python
# Quick test script
import google.generativeai as genai
import os

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not set!")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Say 'Hello from Gemini!' in one sentence.")
    print("✓ API Connection successful!")
    print(response.text)
```

Run this to verify your API key works:
```bash
python test_api.py
```

## Upgrading to Paid Plan

### Why Upgrade?

- **Higher rate limits**: 10,000+ requests per minute
- **Higher daily limits**: 100,000+ requests per day
- **Priority support**: Dedicated support team
- **SLA**: Service level agreements

### How to Upgrade

1. Go to [Google Cloud Billing](https://console.cloud.google.com/billing)
2. Set up a payment method
3. Enable billing for your project
4. Upgrade to paid tier
5. No changes needed to your code!

## Support and Resources

### Documentation
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [API Reference](https://ai.google.dev/api/rest)
- [Model Documentation](https://ai.google.dev/models/gemini-pro)

### Troubleshooting
- [Common Issues](https://ai.google.dev/docs/troubleshooting)
- [GitHub Issues](https://github.com/aiMahdiX/Medical_VisionTest/issues)
- [Google Support](https://support.google.com/cloud)

### Community
- Stack Overflow: Tag with `google-generativeai`
- GitHub Discussions: Join our community
- Discord/Reddit: AI community forums

## Frequently Asked Questions

**Q: Is the API free?**
A: Yes, with usage limits. Free tier includes 60 requests/minute.

**Q: What if I exceed the rate limit?**
A: Application uses local ML analysis as fallback. You can also upgrade to paid plan.

**Q: Is my API key safe?**
A: Yes, stored locally only. Never transmitted or stored in cloud unless you commit it.

**Q: Can I use the same key on multiple devices?**
A: Yes, but rate limits apply across all devices using that key.

**Q: What models are available?**
A: Gemini 1.5 Pro, Gemini 1.5 Flash, and Gemini 2.0 Flash. See documentation for details.

**Q: Do I need a Google Cloud project?**
A: No, you can use Google AI Studio for quick setup. Project recommended for production.

---

For application-specific issues, see [README.md](README.md)
For general setup issues, refer to [INSTALLATION.md](INSTALLATION.md)
