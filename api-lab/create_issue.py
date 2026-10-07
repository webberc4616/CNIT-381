import os
import requests

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "webberc4616" # <-- change to your GitHub username
REPO = "CNIT-381"

url = f"https://api.github.com/repos/{USERNAME}/{REPO}/issues"
headers = {
 "Authorization": f"Bearer {TOKEN}",
 "Accept": "application/vnd.github+json",
 "User-Agent": USERNAME,
}
payload = {
 "title": "Created from the CNIT 381 API lab",
 "body": "This issue was created with a POST request from Python.",
}

resp = requests.post(url, headers=headers, json=payload)
resp.raise_for_status()
issue = resp.json()
print("Created issue #", issue["number"])
print("View it at:", issue["html_url"])
