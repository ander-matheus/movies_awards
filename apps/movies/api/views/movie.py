from http import HTTPMethod

from django.db.models import ExpressionWrapper, F, IntegerField, Max, Min, Window
from django.db.models.functions import Lag
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.movies.models import Movie, Producer

from ..serializers import AwardsIntervalSerializer, MovieSerializer


class MovieViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for read-only operations on movies.

    Actions:
        list (MovieSerializer): Returns a paginated list of movies.
        retrieve (MovieSerializer): Returns details of a specific movie.
        awards_interval_by_producer (AwardsIntervalSerializer): Calculates intervals
         between 'Worst Picture' awards for producers.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    search_fields = ["title"]

    @extend_schema(responses={200: AwardsIntervalSerializer})
    @action(
        detail=False, methods=[HTTPMethod.GET], url_path="awards-interval-by-producer"
    )
    def awards_interval_by_producer(self, request):
        """
        Calculates the minimum and maximum intervals between consecutive 'Worst Picture'
          awards for producers.

        Endpoint: GET /movies/awards-interval-by-producer/

        Returns:
            AwardsIntervalSerializer: Contains:
                - min (AwardsIntervalSerializer): List of producers with the shortest
                  interval between awards.
                - max (AwardsIntervalSerializer): List of producers with the longest
                  interval between awards.

        Notes:
            1. Only considers producers with at least two awards.
            2. Uses window functions (LAG) to calculate consecutive award years.
            3. Excludes records without a previous award.
        """
        qs = (
            Producer.objects.filter(movies__winner=True)
            .annotate(
                award_year=F("movies__year"),  # Current year award
                award_last_year=Window(
                    expression=Lag("movies__year"),  # get the last year award
                    partition_by=[F("id")],  # annotate by producer
                    order_by=F("movies__year").asc(),
                ),
            )
            .annotate(
                interval=ExpressionWrapper(
                    F("award_year") - F("award_last_year"), output_field=IntegerField()
                )
            )
            .exclude(award_last_year__isnull=True)
            .values("name", "interval", "award_last_year", "award_year")
        )

        # using window and lag, isn't possible annotate min and max interval
        interval = qs.aggregate(
            max_interval=Max("interval"),
            min_interval=Min("interval"),
        )
        data = {
            "min": qs.filter(interval=interval["min_interval"]),
            "max": qs.filter(interval=interval["max_interval"]),
        }

        return Response(AwardsIntervalSerializer(data).data)
