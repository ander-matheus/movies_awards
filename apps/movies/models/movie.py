from django.db import models


class Movie(models.Model):
    """
    Represents a movie registered in the system.

    Attributes:
        year (int): Release year of the movie.
        title (str): Title of the movie.
        producer (ManyToMany): Producers associated with the movie.
        studio (ManyToMany): Studios associated with the movie.
        winner (bool): Indicates if the movie is an award winner.
    """

    year = models.IntegerField()
    title = models.CharField(max_length=255)
    producer = models.ManyToManyField("movies.Producer", related_name="movies")
    studio = models.ManyToManyField("movies.Studio", related_name="movies")

    winner = models.BooleanField(default=False)

    class Meta:
        ordering = ["year"]

    def __str__(self) -> str:
        return self.title
