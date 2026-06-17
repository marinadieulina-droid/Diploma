# Diploma Project – Test Automation Framework for PPL CZ

## Project Overview

This diploma project demonstrates the development of an automated testing framework for the PPL CZ web application.

The framework was created to support Quality Assurance activities by automating functional and regression testing of the system. 
The solution is implemented using Python, Selenium WebDriver, Pytest, and Allure Report following the Page Object Model (POM) design pattern.

## Project Objectives

The main objectives of the project are:

* Automate repetitive testing activities.
* Improve software quality assurance processes.
* Reduce manual testing effort.
* Increase test coverage of critical business functionality.
* Provide clear and detailed test reporting.

## Technologies Used

* Python 3.13
* Selenium WebDriver
* Pytest
* Allure Report
* Git
* GitHub

## Test Architecture

The framework follows the Page Object Model (POM) design pattern and integrates modern CI/CD practices.

Project structure:

* **pages/** – page objects and business logic.
* **tests/** – automated test scenarios.
* **conftest.py** – browser setup and test fixtures.
* **pytest.ini** – test framework configuration.
* **allure-results/** – raw test execution results.
* **allure-report/** – generated test reports.
* **.github/workflows/** – CI/CD configuration files for automated testing.
* **gh-pages** – branch dedicated to hosting the Allure test reports.

## Implemented Features

The framework includes:

* Automated functional testing.
* Automated regression testing.
* Explicit waits using WebDriverWait.
* Dynamic element synchronization.
* Shadow DOM handling.
* JavaScript-based interactions for complex UI components.
* Allure reporting and analytics.
* CI/CD integration with GitHub Actions.

## Test Coverage

The project currently contains 17 automated test cases covering:

* Homepage functionality.
* Website navigation.
* Language switching.
* Shipment tracking.
* Pickup point search.
* Interactive map functionality.
* Map filters and geolocation.
* Meta tags validation.
* Error page validation (404).

## Running Tests
Execute all tests:
```
pytest
```

## Generate Allure results:
```
pytest --alluredir=allure-results
```

## Generating Allure Report
Generate report:
```
allure generate allure-results --clean -o allure-report

```

Open report locally:
```
allure open allure-report

```

## Test Results

All test executions are documented using Allure Report.

Current project status:

* Total automated tests: 17
* Passed: 17
* Failed: 0

---

## Repository Links

GitHub Repository:

[https://github.com/marinadieulina-droid/Diploma](https://github.com/marinadieulina-droid/Diploma)

Allure Report:

[https://marinadieulina-droid.github.io/Diploma/](https://marinadieulina-droid.github.io/Diploma/)


## Author

Marina Dieulina

Diploma Thesis – QA Engineering and Test Automation