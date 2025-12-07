# Enable Gemini API Free Tier

## ❌ Error: Quota Limit is 0

If you see this error:
```
429 You exceeded your current quota
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0
```

This means the **Gemini API free tier hasn't been enabled** for your Google Cloud project.

## ✅ Step-by-Step Fix

### Step 1: Get Your API Key

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key or use an existing one
4. Copy the API key

### Step 2: Enable Gemini API in Google Cloud Console

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Sign in with the same Google account

2. **Select or Create a Project:**
   - If you don't have a project, create one (it's free)
   - Project name: "Physical AI Textbook" (or any name)

3. **Enable the Generative Language API:**
   - Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   - Click **"Enable"** button
   - Wait for it to enable (usually takes 1-2 minutes)

### Step 3: Set Up Billing (Free Tier - No Credit Card Required)

**Important:** Even the free tier requires a billing account, but you won't be charged if you stay within free limits.

1. **Go to Billing:**
   - Visit: https://console.cloud.google.com/billing
   - Click **"Link a billing account"** or **"Create billing account"**

2. **Create Free Billing Account:**
   - Google offers a **$300 free credit** for new accounts
   - The Gemini API free tier has generous limits
   - You won't be charged if you stay within free tier limits

3. **Link to Your Project:**
   - Select your project
   - Link the billing account

### Step 4: Verify Quota

1. **Check Quota Status:**
   - Visit: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
   - Look for "Generate Requests Per Day Per Project Per Model - Free Tier"
   - The limit should be **> 0** (usually 15 requests/minute, 1500 requests/day)

2. **Wait 5-10 Minutes:**
   - After enabling, wait a few minutes for quotas to activate
   - Refresh the quota page to see updated limits

### Step 5: Test Your API Key

Run this to test:

```bash
cd backend
source venv/bin/activate
python3 LIST_MODELS.py
```

You should see a list of available models. If you get a quota error, wait a few more minutes and try again.

## 📊 Free Tier Limits

According to Google's documentation, the free tier includes:

- **15 requests per minute** (per model)
- **1,500 requests per day** (per model)
- **1 million input tokens per day**
- **500,000 output tokens per day**

These limits are generous for development and testing!

## 🔍 Troubleshooting

### Still Getting "Limit: 0" Error?

1. **Check API is Enabled:**
   - Go to: https://console.cloud.google.com/apis/dashboard
   - Search for "Generative Language API"
   - Make sure it shows "Enabled" (green checkmark)

2. **Check Billing:**
   - Go to: https://console.cloud.google.com/billing
   - Make sure a billing account is linked to your project
   - Even free tier needs billing account (but won't charge you)

3. **Check API Key:**
   - Make sure your API key is from the same Google account
   - Regenerate the key if needed: https://aistudio.google.com/app/apikey

4. **Wait Longer:**
   - Sometimes it takes 10-15 minutes for quotas to activate
   - Check the quota page again after waiting

### Alternative: Use Different Model

If you continue having issues, try using `gemini-pro` instead:

1. Edit `backend/app/gemini_client.py`
2. Change the model order to try `gemini-pro` first
3. This is the original free tier model and may have different quota settings

## 📚 Resources

- **API Key Management:** https://aistudio.google.com/app/apikey
- **API Documentation:** https://ai.google.dev/gemini-api/docs
- **Quota Information:** https://ai.google.dev/gemini-api/docs/quota
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits
- **Google Cloud Console:** https://console.cloud.google.com/

## ✅ Success Indicators

Once everything is set up correctly, you should see:

1. ✅ No "limit: 0" errors
2. ✅ Model successfully initializes: `✅ Using model: gemini-2.0-flash-lite`
3. ✅ Chat responses work without quota errors
4. ✅ Quota page shows limits > 0

If you see these, you're all set! 🎉

