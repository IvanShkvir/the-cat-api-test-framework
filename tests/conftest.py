import json
from pathlib import Path

import allure
import pytest
import yaml
from allure import attachment_type as at
from jsonref import replace_refs

from interfaces.the_cat_api_client import TheCatAPIClient
from utils.config import THE_CAT_API_BASE_URL, THE_CAT_API_KEY


@pytest.fixture(scope='session')
def cat_api_client(request):
    """
    Fixture that initializes the TheCatAPIClient instance with the base URL and API key for TheCatAPI.

    This fixture is scoped to the test session, meaning it is created once per test session and shared
    across all tests that need it.

    Returns:
        TheCatAPIClient: The initialized API client for interacting with TheCatAPI.
    """
    allure.attach(THE_CAT_API_BASE_URL, 'TheCatAPI URL', at.TEXT)
    yield TheCatAPIClient(THE_CAT_API_BASE_URL, THE_CAT_API_KEY)


@pytest.fixture(scope='session')
def swagger(request) -> dict:
    """
    Fixture that loads the Swagger YAML file, located in the 'test_data' folder, and replaces all `$ref`
    occurrences with actual references using the `jsonref.replace_refs` method.

    This fixture is scoped to the test session, meaning it is created once per test session and shared
    across all tests that need the Swagger data.

    Returns:
        dict: The Swagger data with all references replaced.
    """
    swagger_path = Path(__file__).parent.parent / 'test_data' / 'swagger.yaml'
    with open(swagger_path, 'r') as f:
        swagger_data = yaml.safe_load(f)
    swagger_data_dereferenced = replace_refs(swagger_data)  # replaces all $ref occurrences with actual references
    allure.attach(json.dumps(swagger_data_dereferenced, indent=2), 'Swagger', at.JSON)
    yield swagger_data_dereferenced
