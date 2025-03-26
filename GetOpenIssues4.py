import requests
import json
import browser_cookie3  # To grab browser cookies for authentication

# Jira instance
JIRA_API_URL = "https://estjira.slavo.com/rest/api/2/search"
PROJECT_KEY = "JSWCLOUD"
JQL_QUERY = f"project={PROJECT_KEY} AND statusCategory!=Done"

# Request parameters
PARAMS = {
    "jql": JQL_QUERY,
    "startAt": 0,
    "maxResults": 100,
    "fields": ["summary", "status", "created", "updated", "priority"],
}

# Try fetching cookies from your browser
cookies = browser_cookie3.chrome()  # Use Chrome cookies
# cookies = browser_cookie3.firefox()  # Uncomment for Firefox

HEADERS = {"Accept": "application/json"}

all_issues = []
while True:
    response = requests.get(JIRA_API_URL, params=PARAMS, headers=HEADERS, cookies=cookies)
    response.raise_for_status()

    data = response.json()
    issues = data.get("issues", [])
    all_issues.extend(issues)

    # Pagination logic
    PARAMS["startAt"] += len(issues)
    if len(issues) < 100:
        break

# Save to JSON file
with open("open_issues.json", "w", encoding="utf-8") as file:
    json.dump(all_issues, file, indent=4)

print(f"✅ Successfully fetched {len(all_issues)} open issues from {PROJECT_KEY} using SSO!")
