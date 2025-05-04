from rest_framework import serializers

from apps.movies.models import Producer


class ProducerWinnerIntervalSerializer(serializers.ModelSerializer):
    """
    Serializer for representing a producer's interval between winning 'Worst Picture'
      awards.

    Attributes:
        producer (str): Name of the producer.
        interval (int): Number of years between consecutive awards.
        previousWin (int): Year of the previous award.
        followingWin (int): Year of the following award.
    """

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
    """
    Serializer for representing the minimum and maximum intervals between producers' awards.

    Attributes:
        min (list of ProducerWinnerIntervalSerializer): Producers with the shortest
         intervals between awards.
        max (list of ProducerWinnerIntervalSerializer): Producers with the longest
         intervals between awards.
    """

    min = ProducerWinnerIntervalSerializer(many=True)
    max = ProducerWinnerIntervalSerializer(many=True)
