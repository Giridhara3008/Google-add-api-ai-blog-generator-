#  AI Blog Generator with Google Ads API Integration
This Flask web application generates SEO-optimized blog posts using the OpenAI API and keyword ideas from the Google Ads API. It supports Google OAuth for secure access and has a built-in scheduler to automate blog post generation every 24 hours.
##  Features
Google Ads API OAuth2 authentication
Keyword suggestions using Google Keyword Plan API
Blog generation using OpenAI GPT
Markdown to HTML rendering
 Saves blog posts to local disk
 Automated blog generation every 24 hours using APScheduler
## Tech Stack
- Python 3
- Flask
- OpenAI API
- Google Ads API 
- APScheduler
- Markdown
##  Project Structure
ai-blog-generator/
app.py # Main Flask application
ai_generator.py ### Handles OpenAI blog generation
seo_fetcher.py # Fetches SEO keywordideas from Google Ads
google-ads.yaml ## Google Adscredentials
sri.json # Google OAuth client secrets
requirements.txt # Python dependencies
##  1.Steps to do the project 
Created a new Python project folder: ai-blog-generator
Set up a Python virtual environment using venv
## 2.Set Up OpenAI Blog Generator
Created ai_generator.py to integrate OpenAI API:
Used your OPENAI_API_KEY from environment variables.
Wrote a function to generate a blog post based on a keyword or SEO data
## 3.Integrate Google Ads API
Created a Google Cloud project.
Enabled the Google Ads API.
Generated OAuth 2.0 credentials (OAuth Client ID + Secret) and saved them as sri.json.
## Created google-ads.yaml with:
Developer token
Client ID & Secret
Placeholder for refresh token
Login & client customer ID
##  4.OAuth Authentication Flow
Built OAuth flow in Flask:
/authorize route to redirect user to Google login
/oauth2callback to handle the response and extract refresh_token
Displayed the refresh token in HTML so it can be copied into google-ads.yaml.
## Created seo_fetcher.py to:
Load GoogleAdsClient from google-ads.yaml
Use KeywordPlanIdeaService to fetch keyword ideas for a given seed keyword
## Created app.py to connect all parts:
/generate?keyword=... endpoint to:
Fetch keyword ideas
Generate blog content using OpenAI
Convert content to HTML using Markdown
Save it to ~/Documents/blogs folder
Defined helper function save_blog() to manage markdown-to-HTML and saving
## For running use the link
http://127.0.0.1:8080

## Conclusion
This AI-powered Blog Generator demonstrates the practical integration of multiple modern technologies—combining Google Ads API for keyword research and OpenAI’s language model for content creation. By automating the generation of SEO-optimized blog posts through a simple Flask web interface and background scheduling, this project significantly reduces the manual effort involved in creating high-quality blog content.

## Knowledge Gained 
This tool can be extended further with user login, blog storage in a CMS or database, and deployment to cloud platforms. It serves as a strong foundation for building real-world AI content automation tools.





