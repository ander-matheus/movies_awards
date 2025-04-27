from django.db import models


class Movie(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    producer = models.ManyToManyField("movies.Producer", related_name="movies")
    studio = models.ManyToManyField("movies.Studio", related_name="movies")

    winner = models.BooleanField(default=False)

    class Meta:
        ordering = ["year"]

    def __str__(self) -> str:
        return self.name
