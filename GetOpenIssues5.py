import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, request

# Jira OAuth 2.0 credentials
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
AUTH_URL = "https://estjira.slavo.com/oauth2/authorize"
TOKEN_URL = "https://estjira.slavo.com/oauth2/token"
REDIRECT_URI = "http://localhost:8080/callback"

# Jira API
JIRA_API_URL = "https://estjira.slavo.com/rest/api/2/search"
PROJECT_KEY = "JSWCLOUD"
JQL_QUERY = f"project={PROJECT_KEY} AND statusCategory!=Done"

# Flask app to handle OAuth callback
app = Flask(__name__)

@app.route("/")
def login():
    jira = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = jira.authorization_url(AUTH_URL)
    return f"Click <a href='{authorization_url}'>here</a> to authorize."

@app.route("/callback")
def callback():
    jira = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = jira.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    # Fetch Jira issues
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    response = requests.get(JIRA_API_URL, headers=headers, params={"jql": JQL_QUERY, "maxResults": 100})
    issues = response.json()

    return f"<h3>Fetched {len(issues.get('issues', []))} issues!</h3>"

if __name__ == "__main__":
    app.run(port=8080)
