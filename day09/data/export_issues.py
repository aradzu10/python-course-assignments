import requests
import csv


def export_issues(owner, repo, output_file="issues.txt"):
    # GitHub API URL for repository issues
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    # Parameters to fetch all issues (open and closed) and maximize page size
    params = {"state": "all", "per_page": 100, "page": 1}

    headers = {"Accept": "application/vnd.github.v3+json"}

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")

        # Header (Optional, comment out if strict row adherence is needed)
        # writer.writerow(["issue_number", "status", "issue_name", "creation_date"])

        while True:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break

            issues = response.json()

            if not issues:
                break

            for issue in issues:
                # Skip Pull Requests (GitHub API considers PRs as issues)
                if "pull_request" in issue:
                    continue

                row = [
                    issue["number"],
                    issue["state"].upper(),
                    issue["title"],
                    issue["created_at"],
                ]
                writer.writerow(row)

            print(f"Processed page {params['page']}...")
            params["page"] += 1

    print(f"Export complete. Data saved to {output_file}")


# --- Configuration ---
OWNER = "Code-Maven"
REPO = "wis-python-course-2025-10"

if __name__ == "__main__":
    export_issues(OWNER, REPO)
