from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, CommentViewSet, LogViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename="task")
router.register('comments', CommentViewSet, basename="comments")
router.register('logs', LogViewSet, basename="logs")


urlpatterns = router.urls
