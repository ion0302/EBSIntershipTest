from rest_framework.routers import DefaultRouter

from apps.tasks.views import UserListViewSet

router = DefaultRouter()
router.register('users-list', UserListViewSet)

urlpatterns = router.urls
