from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, CommentViewSet, TimeLogViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename="task")
router.register('comments', CommentViewSet, basename="comments")
router.register('time_logs', TimeLogViewSet, basename="time_logs")

urlpatterns = router.urls
