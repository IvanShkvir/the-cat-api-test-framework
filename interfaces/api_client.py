"""
This module provides an abstract base class for interacting with APIs, allowing for standardized HTTP requests
(GET, POST, PUT, DELETE) using the `requests` library. The module can be used as a foundation for
building API clients by extending its functionality.

Logging is integrated using a custom logger from `utils.log`.
"""
import json

import requests
import allure
from allure import attachment_type as at

from utils.log import create_logger

# Initialize a logger for the module
logger = create_logger('api')


class APIClient:
    """
    A generic API client to handle HTTP requests.

    Attributes:
        base_url (str): The base URL for the API. This must be set by subclasses or instances.
    """

    def __init__(self, base_url: str):
        """
        Initializes an APIClient instance with a session and default settings.

        Args:
            base_url (str): The base URL for the API.
        """
        self._session = requests.Session()
        self.base_url = base_url

    @property
    def session(self):
        """
        Provides access to the underlying `requests.Session` instance for advanced configurations.

        Returns:
            requests.Session: The session instance used for all requests.
        """
        return self._session

    def _send_request(self, method: str, endpoint: str, params: dict = None, headers: dict = None,
                            body: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP request to the specified endpoint.

        Args:
            method (str): The HTTP method to use ('get', 'post', 'put', 'delete').
            endpoint (str): The API endpoint (relative to `base_url`).
            params (dict, optional): Query parameters to include in the request URL.
            headers (dict, optional): Headers to include in the request.
            body (dict, optional): JSON body for the request (used for POST, PUT, etc.).
            **kwargs: Additional parameters to pass to the request method.

        Returns:
            requests.Response: The response object from the server.

        Raises:
            ValueError: If an unsupported HTTP method is specified.
        """
        # Construct the full URL
        url = self.base_url + endpoint

        # Map HTTP methods to corresponding session methods
        method_function = {
            'get': self._session.get,
            'post': self._session.post,
            'put': self._session.put,
            'delete': self._session.delete,
        }.get(method.lower(), None)

        if not method_function:
            raise ValueError(f'Unknown method {method}')

        # Log the request details
        logger.info(
            f'Sending {method.upper()} request with parameters url={url}; headers={headers}; body={body}; params={params}')
        allure.attach(json.dumps(url, indent=2), name='Request URL', attachment_type=at.TEXT)
        allure.attach(json.dumps(headers, indent=2), name='Request Headers', attachment_type=at.JSON)
        allure.attach(json.dumps(body, indent=2), name='Request Body', attachment_type=at.JSON)
        allure.attach(json.dumps(params, indent=2), name='Request Params', attachment_type=at.JSON)

        # Send the request
        resp = method_function(url, headers=headers, json=body, params=params, **kwargs)

        # Log the response details
        logger.info(f'Response status - {resp.status_code}, response data - {resp.text}')
        allure.attach(str(resp.status_code), name='Response Status', attachment_type=at.TEXT)
        allure.attach(resp.text, name='Response Body', attachment_type=at.TEXT)

        return resp

    @allure.step('Sending GET request to {endpoint}')
    def get(self, endpoint: str, params: dict = None, headers: dict = None, body: dict = None, **kwargs) -> requests.Response:
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters to include in the request URL.
            headers (dict, optional): Headers to include in the request.
            body (dict, optional): JSON body (rarely used for GET requests).
            **kwargs: Additional request parameters.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request('get', endpoint, params, headers, body, **kwargs)

    @allure.step('Sending POST request to {endpoint}')
    def post(self, endpoint: str, params: dict = None, headers: dict = None, body: dict = None, **kwargs) -> requests.Response:
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters to include in the request URL.
            headers (dict, optional): Headers to include in the request.
            body (dict, optional): JSON body to include in the request.
            **kwargs: Additional request parameters.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request('post', endpoint, params, headers, body, **kwargs)

    @allure.step('Sending PUT request to {endpoint}')
    def put(self, endpoint: str, params: dict = None, headers: dict = None, body: dict = None, **kwargs) -> requests.Response:
        """
        Sends a PUT request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters to include in the request URL.
            headers (dict, optional): Headers to include in the request.
            body (dict, optional): JSON body to include in the request.
            **kwargs: Additional request parameters.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request('put', endpoint, params, headers, body, **kwargs)

    @allure.step('Sending DELETE request to {endpoint}')
    def delete(self, endpoint: str, params: dict = None, headers: dict = None, body: dict = None, **kwargs) -> requests.Response:
        """
        Sends a DELETE request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters to include in the request URL.
            headers (dict, optional): Headers to include in the request.
            body (dict, optional): JSON body to include in the request.
            **kwargs: Additional request parameters.

        Returns:
            requests.Response: The response object.
        """
        return self._send_request('delete', endpoint, params, headers, body, **kwargs)
