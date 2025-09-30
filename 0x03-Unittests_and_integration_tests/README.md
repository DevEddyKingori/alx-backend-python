# 🧪 GitHub Org Client — Unit Testing Project

This project demonstrates how to implement and test a GitHub organization client in Python using **object-oriented programming**, **mocking**, and **unit testing** with Python's built-in `unittest` framework.

It includes:
- A `GithubOrgClient` class that fetches and filters public repositories from GitHub
- A set of utility functions (`get_json`, `access_nested_map`, `memoize`)
- A complete **unit test suite** covering all major methods
- Mocked HTTP requests to avoid real network calls
- Use of `unittest.mock`, `parameterized`, and `PropertyMock`

---

## 📁 Project Structure

```
github_org_client/
│
├── utils.py              # Utility functions
├── client.py             # GithubOrgClient class
├── test_client.py        # Unit tests for GithubOrgClient
├── test_utils.py         # Unit tests for utility functions
├── README.md             # This file
```

---

## 🔧 Features Implemented

### ✅ Utility Functions

| Function | Purpose |
|---------|---------|
| `access_nested_map(nested_map, path)` | Safely access values in deeply nested dictionaries |
| `get_json(url)` | Fetch JSON from a remote URL |
| `memoize(fn)` | Cache the result of a method to avoid recomputation |

### ✅ GithubOrgClient Class

| Method | Description |
|--------|-------------|
| `org()` | Fetches organization data using `get_json` |
| `_public_repos_url` | Property that gets the repo URL from `org()` |
| `repos_payload()` | Fetches repository data from the repo URL |
| `public_repos(license)` | Returns a list of repo names, optionally filtered by license |
| `has_license(repo, license_key)` | Static method to check if a repo has a specific license |

---

## 🧪 Test Coverage

All major functions and methods are covered by unit tests:

### 🧪 `test_utils.py`

| Test Class | Method | Description |
|-----------|--------|-------------|
| `TestAccessNestedMap` | `test_access_nested_map()` | Tests access to values in nested maps |
| `TestAccessNestedMap` | `test_access_nested_map_exception()` | Tests KeyError for invalid paths |
| `TestGetJson` | `test_get_json()` | Tests that `get_json` returns correct data and calls URL once |
| `TestMemoize` | `test_memoize()` | Tests that a method is only called once when accessed multiple times |

### 🧪 `test_client.py`

| Test Class | Method | Description |
|-----------|--------|-------------|
| `TestGithubOrgClient` | `test_org()` | Tests that `org()` returns correct data and calls `get_json` once |
| `TestGithubOrgClient` | `test_public_repos_url()` | Tests that `_public_repos_url` returns the correct URL from mocked `org` |
| `TestGithubOrgClient` | `test_public_repos()` | Tests that `public_repos()` returns correct repo names and filters by license |
| `TestGithubOrgClient` | `test_has_license()` | Tests that license checking works for matching and non-matching cases |

---

## 🔧 Requirements

To run this project, make sure you have the following installed:

```bash
pip install parameterized
```

Python 3.6+ is required.

---

## 🧪 How to Run the Tests

From the root of the project:

```bash
python3 -m unittest test_utils.py -v
python3 -m unittest test_client.py -v
```

Or run all tests at once:

```bash
python3 -m unittest discover
```

All tests should pass without making any real HTTP requests.

---

## 📦 Technologies Used

- **Python 3.x**
- **`unittest`** – For writing and running unit tests
- **`unittest.mock`** – For mocking functions and properties
- **`parameterized`** – For data-driven testing with multiple inputs
- **`PropertyMock`** – For mocking properties in unit tests

---




