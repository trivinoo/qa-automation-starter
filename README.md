# QA Automation Starter Kit & Learning Guide

Welcome to your hands-on QA Automation learning repository. This project is structured to help you understand how modern test automation works across API, Web, and Mobile testing, comparing **Robot Framework**, **Cypress**, **Appium**, and **Python (pytest)**.

---

## 📁 Repository Structure

```
qa-automation-starter/
├── mock_app/
│   └── server.py             # Built-in lightweight test application (Web UI + REST API)
├── python_pytest_api/
│   └── test_api.py           # Python API automation tests (Standard test patterns)
├── robot_suite/
│   └── test_suite.robot      # Robot Framework keyword-driven test suite
├── cypress_e2e/
│   └── spec.cy.js            # Cypress modern browser end-to-end tests
├── appium_mobile/
│   └── appium_sample.py      # Appium mobile test template & capabilities configuration
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🚀 1. The Core QA Automation Landscape

| Tool | Primary Domain | Language | Style / Strength |
|---|---|---|---|
| **Python + Pytest** | API, Integration, Backend | Python | Flexible, huge ecosystem, industry standard |
| **Robot Framework** | Acceptance & End-to-End | Keyword / Tabular DSL (Python-backed) | Readable by non-developers, human-like test cases |
| **Cypress** | Web Front-End / E2E | JavaScript / TypeScript | Fast in-browser execution, automatic waits, time-travel debugging |
| **Appium** | Mobile (iOS & Android) | Multi-language (Python, Java, JS) | Cross-platform standard for native and hybrid mobile apps |

---

## 🛠️ 2. Step-by-Step: How to Run the Included Demos

### Step A: Start the Mock App Under Test
The project includes a self-contained web and API server (no external dependencies needed):
```powershell
python mock_app\server.py
```
This runs at `http://127.0.0.1:8000` with both a web login interface and REST endpoints:
- `GET  /api/health`
- `GET  /api/products`
- `POST /api/login`

### Step B: Run Python API Tests
In a separate terminal:
```powershell
pip install pytest
pytest python_pytest_api\test_api.py -v
```

### Step C: How Robot Framework Works
Robot Framework tests are written in natural, readable keywords:
```robot
*** Test Cases ***
User Authentication Valid Credentials
    ${body}=           Create Dictionary    email=${VALID_USER}    password=${VALID_PASS}
    ${response}=       POST On Session   sut    /api/login    json=${body}
    Status Should Be   200    ${response}
```
To run:
```powershell
pip install robotframework robotframework-requests
robot robot_suite\test_suite.robot
```
Robot Framework automatically outputs detailed visual HTML reports: `report.html` and `log.html`.

### Step D: How Cypress Works
Cypress tests run inside a real browser engine (Chrome, Edge, Firefox) using JavaScript:
```javascript
cy.get('[data-testid="username-input"]').type('student@test.com');
cy.get('[data-testid="login-button"]').click();
cy.get('[data-testid="status-message"]').should('contain.text', 'Login successful');
```
To run Cypress:
```powershell
npm init -y
npm install cypress --save-dev
npx cypress open
```

### Step E: How Appium Works
Appium operates as an HTTP server that translates standard WebDriver actions into native OS automation commands (via `UiAutomator2` on Android or `XCUITest` on iOS).
To use Appium:
1. Install Node.js and Appium CLI: `npm install -g appium`
2. Install Android driver: `appium driver install uiautomator2`
3. Install Python client: `pip install Appium-Python-Client`
4. Review [`appium_mobile/appium_sample.py`](appium_mobile/appium_sample.py) for the driver setup and locator patterns.

---

## 📌 Pushing This Repository to Your GitHub

This folder has already been initialized as a Git repository. To connect it to your GitHub profile:

1. Create a new empty repository on [GitHub](https://github.com/new) (e.g. named `qa-automation-starter`).
2. Run these commands in your PowerShell:
```powershell
cd C:\Users\trivi\.gemini\antigravity\scratch\qa-automation-starter
git remote add origin https://github.com/trivinoo/<YOUR-REPO-NAME>.git
git branch -M main
git push -u origin main
```
*(GitHub will prompt you for authentication via browser or a Personal Access Token).*
