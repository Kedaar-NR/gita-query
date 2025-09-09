(AI-Generated Guide on Deploying to Streamlit)
# Deployment Guide

## Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** for your chatbot
2. **Upload all files** from this project to your repository
3. **Ensure these files are included**:
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `runtime.txt` (Python version specification)
   - `rag/` folder (all RAG components)
   - `.streamlit/config.toml` (configuration)
   - `README.md` (documentation)

### Step 2: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the details**:
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Choose a unique name (e.g., `gita-chatbot`)

### Step 3: Configure Secrets (Optional)

If you want to use Gemini or OpenAI APIs:

1. **In your Streamlit Cloud dashboard**, go to your app
2. **Click "Settings"** → **"Secrets"**
3. **Add your API keys**:
   ```toml
   GOOGLE_API_KEY = "your_google_api_key_here"
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

### Step 4: Deploy

1. **Click "Deploy!"**
2. **Wait for the build** (usually 2-5 minutes)
3. **Your app will be live** at `https://your-app-name.streamlit.app`

## Troubleshooting

### Build Fails
- Check that all files are in the repository
- Ensure `requirements.txt` has all dependencies
- **Python 3.13 compatibility issue**: If you see pandas compilation errors, the `runtime.txt` file specifies Python 3.11.9 which is compatible with all dependencies
- Check the build logs for specific errors

### App Loads But Shows Errors
- Verify the dataset can be downloaded (Hugging Face access)
- Check that all Python imports work
- Look at the app logs in Streamlit Cloud dashboard

### Slow Performance
- The first load builds the search index (takes 1-2 minutes)
- Subsequent loads are much faster
- Consider using a smaller dataset for testing

## Environment Variables

The app works with these environment variables:

- `GOOGLE_API_KEY`: For Gemini integration (optional)
- `OPENAI_API_KEY`: For OpenAI integration (optional)

Without these keys, the app uses extractive answers (still fully functional).

## Custom Domain (Optional)

Streamlit Cloud supports custom domains:

1. **In your app settings**, go to "Custom domain"
2. **Add your domain** (requires DNS configuration)
3. **Follow the SSL certificate setup**

## Monitoring

- **Usage stats**: Available in your Streamlit Cloud dashboard
- **Error logs**: Check the "Logs" tab in your app dashboard
- **Performance**: Monitor load times and user interactions
