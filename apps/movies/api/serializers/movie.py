from rest_framework import serializers

from apps.movies.models import Movie


class LookupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
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
