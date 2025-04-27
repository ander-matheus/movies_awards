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
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    search_fields = ["title"]

    @extend_schema(responses={200: AwardsIntervalSerializer})
    @action(
        detail=False, methods=[HTTPMethod.GET], url_path="awards-interval-by-producer"
    )
    def awards_interval_by_producer(self, request):
        qs = (
            Producer.objects.filter(movies__winner=True)
            .annotate(
                award_year=F("movies__year"),  # Captura o ano da premiação
                award_last_year=Window(
                    expression=Lag(
                        "movies__year"
                    ),  # Acessa o ano da premiação anterior
                    partition_by=[F("id")],  # Agrupa por produtor
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

        # usando em window e lag, não é possível dar um annotate com min e max interval
        interval = qs.aggregate(
            max_interval=Max("interval"),
            min_interval=Min("interval"),
        )
        data = {
            "min": qs.filter(interval=interval["min_interval"]),
            "max": qs.filter(interval=interval["max_interval"]),
        }

        return Response(AwardsIntervalSerializer(data).data)
