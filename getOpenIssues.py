import requests
import json

# Base URL for Jira API
JIRA_API_URL = "https://jira.atlassian.com/rest/api/2/search"
PROJECT_KEY = "JSWCLOUD"
JQL_QUERY = f"project={PROJECT_KEY} AND statusCategory!=Done"

# Request parameters
PARAMS = {
    "jql": JQL_QUERY,
    "startAt": 0,  # Pagination start
    "maxResults": 100,  # Fetch 100 issues per request
    "fields": ["summary", "status", "created", "updated", "priority"],  # Add more fields if needed
}

all_issues = []
while True:
    response = requests.get(JIRA_API_URL, params=PARAMS)
    response.raise_for_status()  # Ensure we stop on HTTP errors
    
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