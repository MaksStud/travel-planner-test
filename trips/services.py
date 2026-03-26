import requests
import logging
from django.conf import settings
from rest_framework import status

logger = logging.getLogger(__name__)


class ArtInstituteService:
    """Art Institute service."""
    def __init__(self):
        self.BASE_URL = settings.ART_INSTITUTE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "TravelPlannerAPI/1.0"
        })

    def is_artwork_valid(self, artwork_id: str) -> bool:
        """
        Checks whether an artwork exists in the Art Institute system based on its ID.
        The technical specifications require validation before adding it to the project.

        :param artwork_id: The ID of the artwork to check.

        :return: True if the artwork exists, False otherwise.
        """
        try:
            logger.info(f"Checking if artwork {artwork_id} exists in the Art Institute system.")
            url = f"{self.BASE_URL}/artworks/{artwork_id}"
            params = {"fields": "id,title"}

            response = self.session.get(url, params=params, timeout=5)

            if response.status_code == status.HTTP_200_OK:
                logger.info(f"Artwork {artwork_id} exists in the Art Institute system.")
                return True
            logger.error(f"Artwork {artwork_id} does not exist in the Art Institute system.")
            return False
        except requests.RequestException:
            logger.error(f"Error checking if artwork {artwork_id} exists in the Art Institute system.")
            return False

    def get_artwork_details(self, artwork_id: str) -> dict | None:
        """
        Get the name or description, if needed for the extension.

        :param artwork_id: The ID of the artwork to get the details.

        :return: The details of the artwork.
        """
        url = f"{self.BASE_URL}/artworks/{artwork_id}"
        logger.info(f"Getting details for artwork {artwork_id} from the Art Institute system.")

        response = self.session.get(url, timeout=5)
        if response.status_code == 200:
            logger.info(f"Details for artwork {artwork_id} found in the Art Institute system.")
            return response.json().get('data')

        logger.error(f"Error getting details for artwork {artwork_id} from the Art Institute system.")
        return None
