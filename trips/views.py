from rest_framework import viewsets, serializers
from django_filters.rest_framework import DjangoFilterBackend
from trips.models import Project, Place
from trips.serializers import ProjectSerializer, PlaceSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_completed']

    def perform_destroy(self, instance):
        if instance.places.filter(is_visited=True).exists():
            raise serializers.ValidationError(
                {"error": "Cannot delete project because it has visited places."}
            )
        instance.delete()


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'is_visited']

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
