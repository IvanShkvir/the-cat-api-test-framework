"""
This file contains a module to interact with TheCatAPI (https://documenter.getpostman.com/view/5578104/RWgqUxxh#intro).
"""
import allure
from allure import attachment_type as at

from interfaces.api_client import APIClient
from utils.log import create_logger

logger = create_logger('the-cat-api')


class TheCatAPIClient(APIClient):
    """
    A client to interact with TheCatAPI.

    This class extends the APIClient to provide convenient methods for interacting with the endpoints of
    TheCatAPI, including image search, favorites, breeds, votes, facts, and webhooks.

    Attributes:
        base_url (str): The base URL for TheCatAPI.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initializes an instance of TheCatAPIClient.

        Args:
            base_url (str): The base URL for TheCatAPI.
            api_key (str): The API key for authenticating with TheCatAPI.
        """
        super(TheCatAPIClient, self).__init__(base_url)
        self._session.headers.update({'x-api-key': api_key})

    ### Images endpoints ###

    @allure.step('Search for images')
    def images_search(self, **kwargs):
        """
        Searches for cat images using TheCatAPI.

        Args:
            **kwargs: Additional query parameters to be passed into the search.

        Returns:
            requests.Response: The response object from the server containing search results.
        """
        endpoint = '/images/search'

        logger.info(f'Searching cat images with parameters {kwargs}')
        allure.attach(str(kwargs), 'Search parameters', at.TEXT)
        resp = self.get(endpoint, **kwargs)
        return resp

    @allure.step('Get image by ID {image_id}')
    def images_get(self, image_id: str, **kwargs):
        """
        Retrieves an image by its ID from TheCatAPI.

        Args:
            image_id (str): The ID of the image to retrieve.
            **kwargs: Additional query parameters for the request.

        Returns:
            requests.Response: The response object from the server containing the image data.
        """
        endpoint = f'/images/{image_id}'

        logger.info(f'Getting image by its id {image_id}')
        resp = self.get(endpoint, **kwargs)
        return resp

    ...

    ### Favourites endpoints ###
    ...

    ### Breeds endpoints ###
    ...

    ### Votes endpoints ###
    ...

    ### Facts endpoints ###
    ...

    ### Webhooks endpoints ###
    ...
