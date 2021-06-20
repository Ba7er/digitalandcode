from django.db import models

# Create your models here.


class Subject(models.Model):
    subject = models.CharField(max_length=50)
    descrition = models.CharField(max_length=4000)

    def __str__(self):
        return self.subject
