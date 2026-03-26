from rest_framework.routers import DefaultRouter
from trips.views import ProjectViewSet, PlaceViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'places', PlaceViewSet, basename='place')

urlpatterns = router.urls
