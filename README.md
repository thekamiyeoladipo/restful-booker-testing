# Hybrid API + UI Testing Framework

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.60-green)
![Pytest](https://img.shields.io/badge/Pytest-9.0-orange)
![Tests](https://img.shields.io/badge/Tests-11%20Passing-brightgreen)

A hybrid automation testing framework combining API and UI testing, built with Python, Playwright, and Pytest. The framework tests two applications — Restful-Booker (hotel booking API) and DemoQA Bookstore (API + UI) — demonstrating full-stack QA coverage across both layers.

---

## What Makes This a Hybrid Framework

Most automation frameworks test either the UI or the API. This framework tests both — and connects them:

```
Step 1 → Create/modify data via API       (no browser, fast)
Step 2 → Open browser                     (UI layer)
Step 3 → Verify UI correctly reflects API data  (the hybrid assertion)
```

This proves two things at once: the API works correctly, and the UI accurately displays what the API returns.

---

## Framework Architecture

```
restful-booker-testing/
│
├── pages/                    # Page Object Model classes
│   └── demoqa_page.py        # DemoQA bookstore UI interactions
│
├── tests/                    # Test suites
│   ├── test_auth.py          # Restful-Booker authentication tests
│   ├── test_demoqa_api.py    # DemoQA Bookstore API tests
│   └── test_demoqa_ui.py     # DemoQA UI tests including hybrid test
│
├── utils/                    # Helper functions
│   ├── api_helpers.py        # Restful-Booker API utilities
│   └── demoqa_helpers.py     # DemoQA API utilities
│
├── reports/                  # Allure test reports
├── conftest.py               # Pytest fixtures and browser setup
├── pytest.ini                # Pytest configuration
└── .env                      # Environment variables (not committed)
```

---

## Tech Stack

- **Python 3.12** — Core programming language
- **Playwright** — Browser automation and API request context
- **Pytest** — Test framework and runner
- **Requests** — HTTP library for direct API calls
- **Allure** — Visual test reporting
- **python-dotenv** — Environment variable management
- **pytest-rerunfailures** — Automatic retry for flaky tests

---

## Test Coverage

### Restful-Booker Authentication (`test_auth.py`)
- Generate auth token with valid credentials
- Invalid credentials return bad credentials message

### DemoQA Bookstore API (`test_demoqa_api.py`)
- Generate user auth token
- Get all available books
- Add book to user collection and verify in profile
- Invalid credentials return failed status

### DemoQA Bookstore UI + Hybrid (`test_demoqa_ui.py`)
- Bookstore page loads successfully
- Books are displayed on the bookstore page
- Search filters books by title
- Login with valid credentials
- **[Hybrid]** Book added via API appears in UI profile

---

## Key Engineering Decisions

| Decision | Reason |
|---|---|
| Playwright request context for API calls | Keeps everything in one framework, no need for separate tools |
| Token-based auth testing | Mirrors real-world protected API patterns |
| Cleanup before each destructive test | Prevents false failures from leftover test data |
| `wait_until="commit"` for navigation | DemoQA loads heavy ads — commit fires as soon as server responds |
| Retry logic with delay | Handles network instability without masking real failures |

---

## Getting Started

### Prerequisites
- Python 3.8+
- Java JDK (for Allure reports)
- Allure CLI

### Installation

1. Clone the repository
```bash
git clone https://github.com/thekamiyeoladipo/restful-booker-testing.git
cd restful-booker-testing
```

2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
python -m playwright install
```

4. Set up environment variables — create a `.env` file:
```
BASE_URL=https://restful-booker.herokuapp.com
DEMOQA_BASE_URL=https://demoqa.com
DEMOQA_USERNAME=your_username
DEMOQA_PASSWORD=your_password
DEMOQA_USER_ID=your_user_id
```

---

## Running Tests

```bash
# Run all tests
pytest -v

# Run a specific suite
pytest tests/test_demoqa_ui.py -v

# Run a specific test
pytest tests/test_demoqa_ui.py::TestDemoQAUI::test_api_added_book_appears_in_profile -v
```

## Generating Reports

```bash
# Run tests and generate Allure results
pytest -v

# Open interactive Allure report
allure serve reports/allure-results
```

---

## Author
**Kamiye Oladipo**  
QA Engineer  
[GitHub](https://github.com/thekamiyeoladipo) | [LinkedIn](https://www.linkedin.com/in/kamiye-oladipo/)