import requests
import json

# Base URL for Jira API (update to your company's Jira URL)
JIRA_API_URL = "https://estjira.slavo.com/rest/api/2/search"

# Jira authentication (update with your credentials)
USERNAME = "your_username"  # Replace with your Jira username
API_TOKEN = "your_api_token"  # Replace with your Jira API token

# Jira project key and JQL query
PROJECT_KEY = "JSWCLOUD"
JQL_QUERY = f"project={PROJECT_KEY} AND statusCategory!=Done"

# Request parameters
PARAMS = {
    "jql": JQL_QUERY,
    "startAt": 0,  # Pagination start
    "maxResults": 100,  # Fetch 100 issues per request
    "fields": ["summary", "status", "created", "updated", "priority"],  # Add more fields if needed
}

# Headers for authentication
HEADERS = {
    "Accept": "application/json"
}

# List to store all issues
all_issues = []

while True:
    response = requests.get(
        JIRA_API_URL, 
        params=PARAMS, 
        auth=(USERNAME, API_TOKEN),  # Authentication
        headers=HEADERS
    )
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
