from django.db import models


class Studio(models.Model):
    """
    Represents a movie studio.

    Attributes:
        name (str): Name of the studio.
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
