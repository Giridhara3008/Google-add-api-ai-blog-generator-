from flask import Flask, request, jsonify, redirect, session
import markdown
import os
from datetime import datetime
from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post
from google.ads.googleads.client import GoogleAdsClient
from google_auth_oauthlib.flow import Flow
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OAuth2 config
CLIENT_SECRETS_FILE = "/Users/giridharasrikarchittem/Desktop/ai-blog-generator-interview-srikar chittem/sri.json"
SCOPES = ['https://www.googleapis.com/auth/adwords']
REDIRECT_URI = 'http://127.0.0.1:8080/oauth2callback'

# Load Google Ads config path from env
GOOGLE_ADS_YAML_PATH = os.getenv("GOOGLE_ADS_YAML_PATH")
GOOGLE_CUSTOMER_ID = os.getenv("GOOGLE_CUSTOMER_ID")

@app.route("/")
def index():
    return "App is running. <a href='/authorize'>Start Google OAuth</a>"

@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    state = session.get('state')
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    refresh_token = credentials.refresh_token

    return f"""
    <h2>Authentication Successful!</h2>
    <p><strong>Refresh Token:</strong> {refresh_token}</p>
    <p>Copy this token into your <code>google-ads.yaml</code>:</p>
    <pre>
developer_token: YOUR_DEV_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: {refresh_token}
login_customer_id: {GOOGLE_CUSTOMER_ID or 'YOUR_CUSTOMER_ID'}
    </pre>
    """

@app.route('/generate')
def generate():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'Please provide a keyword'}), 400

    try:
        google_ads_client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)
        seo_data = fetch_seo_data(google_ads_client, GOOGLE_CUSTOMER_ID, keyword)
        if not seo_data:
            return jsonify({'error': 'Failed to fetch SEO data'}), 500

        blog_post = generate_blog_post(keyword, seo_data)
        return save_blog(blog_post)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_blog(blog_post):
    if not blog_post:
        return jsonify({"error": "Empty blog post"}), 400

    html_content = markdown.markdown(blog_post)
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Blog Post</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    output_dir = os.path.expanduser("~/Documents/blogs")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"blog_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    return jsonify({"message": "Blog saved successfully", "path": file_path}), 200

# ----------------------------
# 🔁 Scheduler Job Function
# ----------------------------
def scheduled_blog_job():
    keyword = "latest ai trends"  # You can pull this from a list or DB
    print(f"Running scheduled blog generation for keyword: {keyword}")
    try:
        google_ads_client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML_PATH)
        seo_data = fetch_seo_data(google_ads_client, GOOGLE_CUSTOMER_ID, keyword)
        blog_post = generate_blog_post(keyword, seo_data)
        save_blog(blog_post)
        print("✅ Blog generated and saved successfully.")
    except Exception as e:
        print(f"❌ Scheduled job error: {e}")

# ----------------------------
# 🔁 Start Scheduler
# ----------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_blog_job, 'interval', hours=24)  # Runs every 24 hours
scheduler.start()

if __name__ == '__main__':
    app.run(port=8080, debug=True)
