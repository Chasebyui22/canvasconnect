from django.db import models

class CanvasUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name
