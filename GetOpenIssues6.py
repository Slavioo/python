import requests
import json

# Jira Server API URL
JIRA_API_URL = "https://estjira.slavo.com/rest/api/2/search"
PROJECT_KEY = "JSWCLOUD"
JQL_QUERY = f"project={PROJECT_KEY} AND statusCategory!=Done"

# 🔹 Personal Access Token (replace this with your actual PAT)
PERSONAL_ACCESS_TOKEN = "your_personal_access_token"

# Request parameters
PARAMS = {
    "jql": JQL_QUERY,
    "startAt": 0,  # Pagination start
    "maxResults": 100,  # Fetch 100 issues per request
    "fields": ["summary", "status", "created", "updated", "priority"],
}

# Headers with PAT for authentication
HEADERS = {
    "Authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

all_issues = []
while True:
    response = requests.get(JIRA_API_URL, headers=HEADERS, params=PARAMS)
    response.raise_for_status()  # Stop on HTTP errors

    data = response.json()
    issues = data.get("issues", [])
    all_issues.extend(issues)

    # Pagination logic
    PARAMS["startAt"] += len(issues)
    if len(issues) < 100:
        break  # Exit loop when no more results

# Save to JSON file
with open("open_issues.json", "w", encoding="utf-8") as file:
    json.dump(all_issues, file, indent=4)

print(f"✅ Successfully fetched {len(all_issues)} open issues from {PROJECT_KEY}!")
