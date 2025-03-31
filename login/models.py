from django.db import models
from django.conf import settings


# Create your models here.
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to="staticfiles/")
    bio = models.TextField()
    address = models.TextField()
    phone_number = models.PositiveIntegerField()
    wishlist_items = models.JSONField(default={})
    updated_at = models.DateTimeField(auto_now=True)
