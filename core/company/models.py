from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

class Company(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    # Otros campos relevantes
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(unique=True)  # Mantener unique=True
    username = models.CharField(max_length=150, unique=False)  # Agregar campo username único

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def profile(self):
        profile = Profile.objects.get(user=self)
    
    class Meta:
        unique_together = ('email', 'company')  # Índice único compuesto

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    # Otros campos relevantes
    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=CustomUser)
post_save.connect(save_user_profile, sender=CustomUser)