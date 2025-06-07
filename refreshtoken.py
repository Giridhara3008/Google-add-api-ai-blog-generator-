from google_auth_oauthlib.flow import InstalledAppFlow

def main():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": "970913117906-lne4cb9n5iko3i422ki26m02rs76dsnd.apps.googleusercontent.com",
                "client_secret": "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",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    print(f"\n👉 Go to this URL in your browser:\n{auth_url}")

    code = input("\n🔑 Paste the authorization code here: ")
    flow.fetch_token(code=code)

    print(f"\n✅ Your refresh token is:\n{flow.credentials.refresh_token}")








if __name__ == "__main__":
    main()
