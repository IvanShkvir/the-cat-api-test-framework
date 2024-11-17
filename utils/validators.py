"""
This file contains utility functions for different validations.
"""
import pytest
from jsonschema import validate, ValidationError


def validate_response(response_data: dict, schema_path_keys: [str], swagger: dict):
    """
    Validates the response data against a schema from the Swagger specification.

    This function traverses the Swagger specification using the provided schema path keys,
    retrieves the corresponding schema, and validates the response data against it.

    Args:
        response_data (dict): The response data to validate.
        schema_path_keys (list[str]): A list of keys used to navigate through the Swagger
                                      specification to locate the desired schema.
        swagger (dict): The Swagger specification (the full API documentation in JSON/YAML format).

    Raises:
        ValueError: If the provided schema path is invalid or doesn't exist in the Swagger specification.
        pytest.fail: If the response data does not conform to the schema.
    """
    schema = swagger
    for key in schema_path_keys:
        try:
            schema = schema[key]
        except KeyError:
            raise ValueError(f'Invalid path {schema_path_keys} for the schema')

    try:
        validate(instance=response_data, schema=schema)
    except ValidationError as e:
        pytest.fail(f'Invalid response: {e.message}')
