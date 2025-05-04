from rest_framework import serializers

from apps.movies.models import Movie


class LookupSerializer(serializers.Serializer):
    """
    Serializer for representing simple lookup objects.

    Attributes:
        id (int): Unique identifier.
        name (str): Name of the related object.
    """

    id = serializers.IntegerField()
    name = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model, including related studios and producers.

    Attributes:
        studios (LookupSerializer): List of associated studios.
        producers (LookupSerializer): List of associated producers.
    """

    studios = LookupSerializer(many=True, read_only=True, source="studio")
    producers = LookupSerializer(many=True, read_only=True, source="producer")

    class Meta:
        model = Movie
        fields = [
            "id",
            "year",
            "title",
            "winner",
            "studios",
            "producers",
        ]
