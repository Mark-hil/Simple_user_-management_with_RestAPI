from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
