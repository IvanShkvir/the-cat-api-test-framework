import allure
import pytest

from interfaces.the_cat_api_client import TheCatAPIClient
from utils.validators import validate_response


@allure.suite('/image/search Endpoint')
@pytest.mark.image_search
class TestImagesSearch:
    """
    Test suite for the `/images/search` endpoint of TheCatAPI.
    """

    @allure.title('Validate schema for authorized user\'s image search')
    def test_schema_validation_for_authorized_user(self, cat_api_client: TheCatAPIClient, swagger: dict):
        """
        Validates the schema of the response for an authorized user when searching for images.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.

        Asserts:
            - Response status code is 200.
            - Response schema matches the expected Swagger definition.
        """
        resp = cat_api_client.images_search()

        assert resp.status_code == 200, 'Incorrect status code'
        validate_response(resp.json(), ['components', 'schemas', 'ImagesSearchAuthorizedResponse'], swagger)

    @allure.title('Validate schema for unauthorized user\'s image search')
    def test_schema_validation_for_not_authorized_user(self, cat_api_client: TheCatAPIClient, swagger: dict):
        """
        Validates the schema of the response for an unauthorized user when searching for images.

        Temporarily removes the API key from the session headers for testing.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.

        Asserts:
            - Response status code is 200.
            - Response schema matches the expected Swagger definition.
        """
        api_key = cat_api_client.session.headers.pop('x-api-key')
        try:
            resp = cat_api_client.images_search()
        finally:
            # to not break other tests if something happens (because cat_api_client has a scope='session')
            cat_api_client.session.headers.update({'x-api-key': api_key})

        assert resp.status_code == 200, 'Incorrect status code'
        validate_response(resp.json(), ['components', 'schemas', 'ImagesSearchNotAuthorizedResponse'], swagger)
    
    @pytest.mark.parametrize(
        'limit, num_of_returned_images', 
        [
            (1, 1),
            (15, 15),
            (25, 25),
            # 25 is the highest value for the limit according to the documentation,
            # so everything above has to return only 25 images
            (26, 25),
            (50, 25),
        ]
    )
    @allure.title('Validate \'limit\' parameter in image search')
    def test_valid_limit_parameter(self, cat_api_client: TheCatAPIClient, swagger: dict, limit: int, num_of_returned_images: int):
        """
        Validates that the `limit` parameter works as expected in the `/images/search` endpoint.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.
            limit (int): The requested number of images.
            num_of_returned_images (int): The expected number of returned images.

        Asserts:
            - The number of images in the response matches the expected number.
        """
        resp = cat_api_client.images_search(params={'limit': limit})
        images = resp.json()
        assert len(images) == num_of_returned_images, \
            f'Incorrect number of images, expected - {num_of_returned_images}, actual - {len(images)}'

    @pytest.mark.parametrize('has_breeds', [True, False])
    @allure.title('Validate \'has_breeds\' parameter in image search')
    def test_valid_has_breeds_parameter(self, cat_api_client: TheCatAPIClient, swagger: dict, has_breeds: bool):
        """
        Validates that the `has_breeds` parameter works as expected in the `/images/search` endpoint.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.
            has_breeds (bool): Indicates whether images should have associated breeds.

        Asserts:
            - Response status code is 200.
            - Images in the response comply with the `has_breeds` condition.
        """
        resp = cat_api_client.images_search(params={'limit': 25, 'has_breeds': has_breeds})
        assert resp.status_code == 200, 'Incorrect status code'

        incorrect_images = []
        for image in resp.json():
            image_breeds = image.get('breeds')
            if has_breeds:
                if not image_breeds:
                    incorrect_images.append(image['id'])
            elif not has_breeds:
                if image_breeds:
                    incorrect_images.append(image['id'])
        assert incorrect_images == [], f'Some image(s){' don\'t' if has_breeds else ''} have breads'

    @pytest.mark.parametrize(
        'parameter, value',
        [
            ('limit', -1),
            ('limit', 'qwerty'),
            ('has_breeds', 123),
            ('has_breeds', 'qwerty'),
        ]
    )
    @allure.title('Validate invalid query parameters in image search')
    def test_invalid_query_parameter(self, cat_api_client: TheCatAPIClient, swagger: dict, parameter: str, value):
        """
        Validates the behavior of the `/images/search` endpoint with invalid query parameters.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.
            parameter (str): The name of the query parameter.
            value: The invalid value for the query parameter.

        Asserts:
            - Response status code is 400.
            - Response text matches the expected error description.
        """
        expected_response_text = swagger['paths']['/images/search']['get']['responses']['400']['description']

        resp = cat_api_client.images_search(params={parameter: value})
        assert resp.status_code == 400, 'Incorrect status code'
        assert resp.text == expected_response_text, 'Incorrect response text'


@allure.suite('/images/{image_id} Endpoint')
@pytest.mark.image_get
class TestImagesGet:
    """
    Test suite for the `/images/{image_id}` endpoint of TheCatAPI.
    """

    @allure.title('Validate schema for authorized user\'s image retrieval')
    def test_schema_validation_for_authorized_user(self, cat_api_client: TheCatAPIClient, swagger: dict):
        """
        Validates the schema of the response for an authorized user retrieving an image by ID.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.

        Asserts:
            - Response status code is 200.
            - Response schema matches the expected Swagger definition.
        """
        valid_image_id = 'D2J3R7sUq'

        resp = cat_api_client.images_get(valid_image_id)
        assert resp.status_code == 200, 'Incorrect status code'
        validate_response(resp.json(), ['components', 'schemas', 'ImageAuthorizedResponse'], swagger)

    @allure.title('Validate schema for unauthorized user\'s image retrieval')
    def test_schema_validation_for_unauthorized_user(self, cat_api_client: TheCatAPIClient, swagger: dict):
        """
        Validates the schema of the response for an unauthorized user retrieving an image by ID.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.

        Asserts:
            - Response status code is 200.
            - Response schema matches the expected Swagger definition.
        """
        valid_image_id = 'D2J3R7sUq'

        resp = cat_api_client.images_get(valid_image_id)
        assert resp.status_code == 200, 'Incorrect status code'
        validate_response(resp.json(), ['components', 'schemas', 'ImageNotAuthorizedResponse'], swagger)

    @pytest.mark.parametrize('image_id', ['qwerty12345', '12345', 'q' * 10000])
    @allure.title('Validate incorrect image ID in image retrieval')
    def test_incorrect_image_id_parameter(self, cat_api_client: TheCatAPIClient, swagger: dict, image_id: str):
        """
        Validates the behavior of the `/images/{image_id}` endpoint with invalid image IDs.

        Args:
            cat_api_client (TheCatAPIClient): TheCatAPI client fixture.
            swagger (dict): The Swagger specification fixture.
            image_id (str): The invalid image ID.

        Asserts:
            - Response status code is 400.
            - Response text matches the expected error description.
        """
        expected_response_text = swagger['paths']['/images/{image_id}']['get']['responses']['400']['description'].format(image_id=image_id)

        resp = cat_api_client.images_get(image_id)
        assert resp.status_code == 400, 'Incorrect status code'
        assert resp.text == expected_response_text, 'Incorrect response text'
