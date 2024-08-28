from django.db import models
from company.models import CustomUser
# Create your models here.

class Client(models.Model):
    emails = models.EmailField()
    names = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client of {self.user.email}"
    
