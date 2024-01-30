import pytest
import requests

BASE_URL = "https://api.github.com"

OWNER = "topq-practice"
REPO_NAME = "api-practice"

TOKEN = "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"


class TestGitHubAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.initial_issue_count = self.get_open_issue_count()

    def get_open_issue_count(self):
        response = requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues", headers=self.headers, params={"state": "open"})
        assert response.status_code == 200
        issues = response.json()
        return len(issues)

    def get_first_issue_number(self):
        response = requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues", headers=self.headers)
        issues = response.json()
        return issues['number']

    def test_get_all_open_issues(self):
        print(f"Number of open issues: {self.initial_issue_count}")

    def test_get_issues_with_label_practice1(self):
        response = requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues", headers=self.headers, params={"labels": "practice1"})
        assert response.status_code == 200
        issues_practice1 = response.json()
        print(f"Number of issues with label 'practice1': {len(issues_practice1)}")

    def test_create_new_issue(self):
        data = {
            "title": "Shon's issue",
            "body": "This issue was created via REST API from Python by Shon",
            "milestone": None,
            "labels": ["practice1"],
            "assignees": ["topq-practice"]
        }

        response = requests.post(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues", headers=self.headers, json=data)

        assert response.status_code == 201
        #Incremented the self.initial_issue_count here because I posted one more post (checking this in line 57)
        self.initial_issue_count += 1
        new_issue_number = response.json()["number"]
        print(f"New issue created. Issue Number: {new_issue_number}")

    def test_verify_created_issue(self):
        response = requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues", headers=self.headers)
        assert response.status_code == 200
        issues = response.json()
        assert self.initial_issue_count == len(issues)
        assert issues[0]["title"] == "Shon's issue"

    def test_05_update_created_issue(self):
        response = requests.patch(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues/{self.get_first_issue_number}", headers=self.headers, json={"state": "closed", "state_reason": "not_planned"})
        assert response.status_code == 200
        print("Issue state updated to closed with state_reason: not_planned")

    def test_06_verify_closed_issue(self):
        response = requests.get(f"{BASE_URL}/repos/{OWNER}/{REPO_NAME}/issues", headers=self.headers)
        assert response.status_code == 200
        issues = response.json()
        assert len(issues) == self.initial_issue_count