from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename="task")
router.register('comments', CommentViewSet, basename="comments")

urlpatterns = router.urls
