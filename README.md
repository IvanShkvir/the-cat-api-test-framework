# API Test Framework for The Cat API
This repository provides a scalable, extendable, and flexible test framework for validating API responses from The Cat API. 
The framework is built with Pytest, Requests and Allure.

## Features
* **Endpoint Coverage:**
    * /images/search: Validate schema, query parameters, and error handling.
    * /images/{image_id}: Validate schema and error handling for invalid IDs.
* **Schema Validation:**  
  Uses Swagger specifications (swagger.yaml) to validate API responses.
* **Parameterized Testing:**  
  Handles different combinations of query parameters for comprehensive coverage.
* **Report Generation:**  
  Generates detailed HTML and Allure reports for test results.
* **Reusable Fixtures:**  
  Configures an API client and Swagger data for efficient testing.

---

## Setup instructions
**Prerequisits:**
* Python 3.8+ (You can check python version by running `python --version`)
* Git (You can check Git installation by running `git --version`)

1. **Clone the repository**  
```bash
git clone https://github.com/IvanShkvir/the-cat-api-test-framework.git
cd <repository-folder>
```
2. **Create a Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate   # For Linux/Mac
venv\Scripts\activate       # For Windows
```
3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
4. **Obtain API key from https://thecatapi.com.**  
   Press "GET YOUR API KEY", then "GET FREE ACCESS", 
   enter your email, provide very brief description about the application (can be anything), choose "Personal Project"
   and click "SUBMIT". In your email you will see the mail with API key that has to look like `live_m3Dpjeispqc...`.
5. **Set Environment Variables**
   Set the API key obtained in previous step as an environment variable. You can do this in multiple ways 
   (create `.env` file,configure in IDE, use CLI, etc.). Here is how you can do this using CLI:
```bash
export THE_CAT_API_KEY=<your-cat-api-key>    # Linux/Mac
set THE_CAT_API_KEY=<your-cat-api-key>       # Windows   
```

---

## Run Tests

### Test Execution
To run all tests, in the root folder of framework simply execute:
```bash
pytest
```
To run specific test suites you can use pytest marks:
```bash
pytest -m <mark>
```
For example:
```bash
pytest -m image_search
```

### Test Reports
By default, test execution generate Pytest report in `./test_reports/pytest` and Allure results (not report)
in `./test_reports/allure/results`. These paths are specified in `pytest.ini`.  
If you need other location for reports you can either change the `pytest.ini` or override values when running tests:
```bash
pytest --html=<new-pytest-report-location> --alluredir=<new-allure-results-location>
```

To see the Pytest report simply open the generated `html` file.  
To see the Allure report you have to firstly transform it into `html` file. You can do this with following command:
```bash
allure generate --single-file <path-to-allure-results> --clean -o <path-where-generate-html-report> 
```
After execution, you will be able to open the report as a standalone `html` file.

---

## **Test Cases**

The Cat API has its own API specification ([link](https://raw.githubusercontent.com/thatapicompany/apis/main/theCatAPI.com/thecatapi-oas.yaml)).
But it was badly written, and it doesn't represent the actual implementation of the API. So based on
this old specification the new one was created, but only for two endpoints: 
`/images/search` and `/images/{image_id}`. It doesn't exactly represent the 
current implementation of the API as well, but it can be used for the testing purposes
as a starting point. The new specification is located in `./test_data/swagger.yaml`.  

As an example were implemented a few test cases for two endpoints. Here is the brief description of test cases: 

### 1. `/images/search`
- **Schema Validation**:
  - Validates response schemas for authorized and unauthorized users.
- **Query Parameter Validation**:
  - `limit`: Tests various valid and invalid values for the `limit` parameter.
  - `has_breeds`: Tests the filtering behavior for images with or without breeds.
- **Error Handling**:
  - Ensures the correct error response for invalid query parameters.

### 2. `/images/{image_id}`
- **Schema Validation**:
  - Validates response schemas for valid and invalid `image_id` values.
- **Error Handling**:
  - Ensures proper error handling for invalid or malformed image IDs.

---
