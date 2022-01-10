from django.db import models
from django.contrib.auth.models import User


class Sugar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.DecimalField(max_digits=4, decimal_places=2)
    dt = models.DateTimeField()

    def __str__(self):
        return f'{self.user},{self.index},{self.dt.date()},{self.dt.time()}'
