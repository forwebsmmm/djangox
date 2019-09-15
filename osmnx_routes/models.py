from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class GeoPoints(models.Model):
    route_name = models.CharField(max_length=100)
    point_a = models.FloatField(max_length=50)
    point_b = models.FloatField(max_length=50)
    point_c = models.FloatField(max_length=50)
    point_d = models.FloatField(max_length=50)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    route_view = models.TextField(null=True)

    def __str__(self):
        return self.route_name

    def get_absolute_url(self):
        return reverse('home')