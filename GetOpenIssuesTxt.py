import json
import csv

# Load JSON data from file
with open("open_issues.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # This is a list, not a dict!

# Define CSV file and column headers
csv_filename = "open_issues.csv"
headers = ["Key", "Summary", "Status", "Status Category", "Created", "Updated"]

# Open CSV file and write data
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write header row

    for issue in data:  # Directly iterate over the list
        key = issue.get("key", "")
        fields = issue.get("fields", {})
        summary = fields.get("summary", "")
        status = fields.get("status", {}).get("name", "")
        status_category = fields.get("status", {}).get("statusCategory", {}).get("name", "")
        created = fields.get("created", "")
        updated = fields.get("updated", "")

        writer.writerow([key, summary, status, status_category, created, updated])

print(f"CSV file '{csv_filename}' successfully created with {len(data)} issues!")
