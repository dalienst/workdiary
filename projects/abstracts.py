from django.db import models


class AbstractProjectModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # start_date = models.DateField()
    # end_date = models.DateField()

    class Meta:
        abstract = True
