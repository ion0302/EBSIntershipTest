from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, CommentViewSet, TimeLogViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')
router.register('comments', CommentViewSet, basename="comments")
router.register('timelogs', TimeLogViewSet, basename="timelogs")

urlpatterns = router.urls
