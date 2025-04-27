from rest_framework import serializers

from apps.movies.models import Producer


class ProducerWinnerIntervalSerializer(serializers.ModelSerializer):
    producer = serializers.CharField(source="name")
    interval = serializers.IntegerField()
    previousWin = serializers.IntegerField(source="award_last_year")
    followingWin = serializers.IntegerField(source="award_year")

    class Meta:
        model = Producer

        fields = [
            "producer",
            "interval",
            "previousWin",
            "followingWin",
        ]


class AwardsIntervalSerializer(serializers.Serializer):
    min = ProducerWinnerIntervalSerializer(many=True)
    max = ProducerWinnerIntervalSerializer(many=True)
