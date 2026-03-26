from rest_framework import serializers
from typing import Any
from trips.models import Project, Place
from trips.services import ArtInstituteService


class PlaceSerializer(serializers.ModelSerializer):
    """Place serializer."""
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']

    def validate_external_id(self, value: str) -> str:
        """
        Validate external ID.

        :param value: The external ID.

        :return: The validated external ID.
        """
        service = ArtInstituteService()
        if not service.is_artwork_valid(value):
            raise serializers.ValidationError("Artwork ID does not exist in Art Institute of Chicago.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    """Project serializer."""
    places = PlaceSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places']
        read_only_fields = ['is_completed']

    def create(self, validated_data: dict[str, Any]) -> Project:
        """
        Create project.

        :param validated_data: The validated data.

        :return: The created project.
        """
        places_data = validated_data.pop('places', [])

        if len(places_data) > 10:
            raise serializers.ValidationError("You can add maximum 10 places.")
        project = Project.objects.create(**validated_data)

        for place_data in places_data:
            Place.objects.create(project=project, **place_data)

        return project
