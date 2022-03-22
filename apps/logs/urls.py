from rest_framework.routers import DefaultRouter

from apps.logs.views import LogViewSet

router = DefaultRouter()

router.register('logs', LogViewSet, basename="logs")

urlpatterns = router.urls
