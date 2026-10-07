import os
import requests

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
 raise SystemExit("GITHUB_TOKEN is not set - see Part 1.")

USERNAME = "webberc4616" # <-- change to your GitHub username
REPO = "CNIT-381"


BASE = "https://api.github.com"
HEADERS = {
 "Authorization": f"Bearer {TOKEN}",
 "Accept": "application/vnd.github+json",
 "User-Agent": USERNAME,
}

def get(path, **params):
 resp = requests.get(BASE + path, headers=HEADERS, params=params)
 resp.raise_for_status() # raise on any 4xx / 5xx
 return resp


# Part 2: your repository
resp = get(f"/repos/{USERNAME}/{REPO}")
repo = resp.json()
print("Repo:", repo["full_name"])
print(" description:", repo["description"])
print(" language:", repo["language"])
print(" open issues:", repo["open_issues_count"])
print(" url:", repo["html_url"])
print(" API calls left this hour:", resp.headers.get("X-RateLimit-Remaining"))
print()

# Part 3: handle an error (a repo that does not exist)
try:
 get(f"/repos/{USERNAME}/this-repo-does-not-exist")
except requests.HTTPError as e:
 print("Handled error:", e.response.status_code, "-",
e.response.json().get("message"))
print()

# Part 4: your account
me = get("/user").json()
print("You are:", me["login"], "-", me.get("name"))
print(" public repos:", me["public_repos"])
print()


# Part 5: list your repos (query params + looping a JSON array)
repos = get("/user/repos", per_page=100, sort="updated").json()
print(f"Your {len(repos)} repos (10 most recently updated):")
for r in repos[:10]:
 print(" -", r["name"])