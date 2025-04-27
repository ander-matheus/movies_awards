from rest_framework.routers import DefaultRouter

from apps.movies.api.views import MovieViewSet

router = DefaultRouter()
router.register("movie", MovieViewSet, basename="movie")


urlpatterns = router.urls
