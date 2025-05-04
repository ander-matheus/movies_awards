from django.db import models


class Producer(models.Model):
    """
    Represents a movie producer.

    Attributes:
        name (str): Name of the producer.
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
