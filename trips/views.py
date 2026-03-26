from rest_framework import viewsets, serializers
from django_filters.rest_framework import DjangoFilterBackend
from trips.models import Project, Place
from trips.serializers import ProjectSerializer, PlaceSerializer
from django.db.models import QuerySet


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on projects."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_completed']

    def perform_destroy(self, instance: Project) -> None:
        """
        Delete a project if it has no visited places.

        :param instance: Project instance to delete.
        :return: None.
        :raises serializers.ValidationError: If project contains visited places.
        """
        if instance.places.filter(is_visited=True).exists():
            raise serializers.ValidationError(
                {"error": "Cannot delete project because it has visited places."}
            )
        instance.delete()


class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on places."""

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'is_visited']

    def get_queryset(self) -> QuerySet[Place]:
        """
        Return places filtered by optional project query param.

        :return: Filtered places queryset.
        """
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
